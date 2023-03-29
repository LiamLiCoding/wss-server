import json
import os
import base64
from django.conf import settings
from asgiref.sync import async_to_sync
from django.utils import timezone
from django.shortcuts import reverse
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from django.db.models import ObjectDoesNotExist

from apps.devices.models import Devices, Performance
from apps.record.models import EventLog
from .notification_consumer import _async_send_notification


def send_device_message(device_id, message, message_type="operation"):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('device{}'.format(device_id), {"type": "group_message",
                                                                            "message": message,
                                                                            "message_type": message_type})


class DeviceConsumer(AsyncWebsocketConsumer):
    group_name = ''
    api_key = ''
    device = None
    device_name = ''
    device_enable = False
    user_id = 0

    async def connect(self):
        self.api_key = self.scope["url_route"]["kwargs"].get('api_key', '')
        self.device = await self.get_device()
        if self.device and self.device.is_enable:
            await self.accept()
            self.group_name = 'device{}'.format(self.device.id)
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.update_device_status(active=True)
            message = "Device: {} is online now.".format(self.device.device_name)
            await _async_send_notification(self.user_id, message=message, duration=5000,
                                    jump_url=reverse('device_detail', kwargs={'device_id': self.device.id}))
        else:
            await self.close(code=3003)

    @database_sync_to_async
    def get_device(self):
        try:
            device = Devices.objects.get(api_key=self.api_key)
            if device:
                self.device = device
                self.user_id = device.user.id
                self.device_enable = device.is_enable
                return device
        except ObjectDoesNotExist:
            return

    @database_sync_to_async
    def update_device_status(self, active=True):
        if self.device:
            self.device.last_online = timezone.now()
            self.device.is_activated = True
            self.device.is_active = active
            if active:
                self.device.suc_conv_num += 1
            self.device.save()

    @database_sync_to_async
    def update_device_performance(self, performance_dict):
        if self.device:
            performance = Performance()
            performance.device = self.device
            performance.cpu_rate = performance_dict['cpu_used_rate']
            performance.mem_rate = performance_dict['mem_used_rate']
            performance.disk_write_io = performance_dict['disk_io_read']
            performance.disk_read_io = performance_dict['disk_io_write']
            performance.save()

    @database_sync_to_async
    def save_detect_event(self, event_data):
        data_type = event_data.get('data_type', '')
        file_data = event_data.get('data_file', '')
        intruder_type = event_data.get('intruder_type', 0)
        data_file_name = event_data.get('data_file_name', 0)
        if self.device and data_type and file_data and intruder_type:
            file_data = base64.b64decode(file_data)
            media_path = 'devices/log_img' + data_file_name
            with open(settings.MEDIA_ROOT / media_path, "wb") as f:
                f.write(file_data)

            event_record = EventLog()
            event_record.device = self.device
            event_record.event = intruder_type
            event_record.message = 'intruder event {}'.format(intruder_type)
            event_record.action = 'enter mode'.format(intruder_type)
            event_record.image_url = str(media_path)
            event_record.save()

    async def disconnect(self, close_code):
        await self.update_device_status(active=False)
        if self.device:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            message = "Device: {} is offline now.".format(self.device.device_name)
            await _async_send_notification(self.user_id, message=message, duration=5000, notification_type="warning")

    async def receive(self, text_data=None, bytes_data=None):
        parsed_data = json.loads(text_data)
        message_type = parsed_data.get('message_type')
        message = parsed_data.get('message')

        self.get_device()   # get newest device info

        if not (message_type and message and self.device_enable):
            await self.disconnect(close_code=3003)
            await self.close(code=3003)

        # parse
        if message_type == 'running_performance':
            await self.update_device_performance(message)
        elif message_type == 'detect_event':
            await self.save_detect_event(message)

    async def group_message(self, event):
        print("send device message {}".format(event))
        message_type = event.get('message_type', 'operation')
        data = {"message": event['message'],
                "message_type": message_type}
        await self.send(text_data=json.dumps(data))