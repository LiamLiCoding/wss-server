#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/24 14:40
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer


async def _async_send_notification(user_id, message, notification_type="success", style='', duration=3000, jump_url=''):
    channel_layer = get_channel_layer()
    await channel_layer.group_send('notification-{}'.format(user_id), {"type": "group_message",
                                                                       "message": message,
                                                                       "notification_type": notification_type,
                                                                       "style": style,
                                                                       "duration": duration,
                                                                       "jump_url": jump_url})


def send_notification(user_id, message, notification_type="success", style='', duration=3000, jump_url=''):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('notification-{}'.format(user_id), {"type": "group_message",
                                                                       "message": message,
                                                                       "notification_type": notification_type,
                                                                       "style": style,
                                                                       "duration": duration,
                                                                       "jump_url": jump_url})


class NotificationConsumer(AsyncWebsocketConsumer):
    group_name = ''

    async def connect(self):
        if not self.scope.get('user'):
            await self.close()
        else:
            self.group_name = 'notification-{}'.format(str(self.scope.get('user').id))
            await self.accept()
            await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def group_message(self, event):
        style = event.get('style', '')
        duration = event.get('duration', 3000)
        notification_type = event.get('notification_type', 'success')
        jump_url = event.get('jump_url', '')
        data = {"message": event['message'],
                "duration": duration,
                "style": style,
                "notification_type": notification_type,
                "jump_url": jump_url}
        await self.send(text_data=json.dumps(data))


