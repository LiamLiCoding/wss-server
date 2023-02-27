#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/24 14:40
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

import json
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from django.db.models import ObjectDoesNotExist

from apps.devices.models import Devices


async def send_notification(user_id, message, notification_type="success", style='', duration=3000):
    channel_layer = get_channel_layer()
    await channel_layer.group_send('notification_{}'.format(user_id), {"type": "group_message",
                                                                       "message": message,
                                                                       "notification_type": notification_type,
                                                                       "style": style,
                                                                       "duration": duration})


class DeviceConsumer(AsyncWebsocketConsumer):
    api_key = ''
    device = None
    device_name = ''
    user_id = 0

    async def connect(self):
        self.api_key = self.scope["url_route"]["kwargs"].get('api_key', '')
        self.device = await self.get_device()
        if self.device and self.device.is_enable:
            await self.accept()
            await self.update_device(active=True)
            print(self.user_id)
            message = "Device: {} is online now.".format(self.device.device_name)
            await send_notification(self.user_id, message=message, duration=5000)
        else:
            await self.close(code=3003)

    @database_sync_to_async
    def get_device(self):
        try:
            device = Devices.objects.get(api_key=self.api_key)
            if device:
                self.device = device
                self.user_id = device.user.id
                return device
        except ObjectDoesNotExist:
            return

    @database_sync_to_async
    def update_device(self, active=True):
        if self.device:
            self.device.last_online = timezone.now()
            self.device.is_activated = True
            self.device.is_active = active
            self.device.save()

    async def disconnect(self, close_code):
        await self.update_device(active=False)
        message = "Device: {} is offline now.".format(self.device.device_name)
        await send_notification(self.user_id, message=message, duration=5000, notification_type="warning")

    async def receive(self, text_data=None, bytes_data=None):
        self.device = await self.get_device()   # get the newest database info
        if self.device and self.device.is_enable:
            print('Websocket:Receive message:{}'.format(text_data))
            await self.send(text_data=text_data)
        else:
            await self.disconnect(close_code=3003)
            await self.close(code=3003)


class NotificationConsumer(AsyncWebsocketConsumer):
    group_name = ''

    async def connect(self):
        if not self.scope.get('user'):
            await self.close()
        else:
            self.group_name = 'notification_{}'.format(str(self.scope.get('user').id))
            await self.accept()
            await self.channel_layer.group_add(self.group_name, self.channel_name)

            data = {"message": "Welcome to WSS-web, {} !".format(self.scope.get('user').username),
                    "duration": 3000,
                    "style": "gradient"}
            await self.send(text_data=json.dumps(data))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def group_message(self, event):
        style = event.get('style', '')
        duration = event.get('duration', 3000)
        notification_type = event.get('notification_type', 'success')
        data = {"message": event['message'],
                "duration": duration,
                "style": style,
                "notification_type": notification_type}
        await self.send(text_data=json.dumps(data))


