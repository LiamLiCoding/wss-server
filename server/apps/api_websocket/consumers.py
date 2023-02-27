#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/24 14:40
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer


class DeviceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print(self.scope)

    async def disconnect(self, close_code):
        print("Websocket:connection closed, close code={}".format(close_code))

    async def receive(self, text_data=None, bytes_data=None):
        print('Websocket:Receive message:{}'.format(text_data))
        await self.send(text_data=text_data)


class NotificationConsumer(AsyncWebsocketConsumer):
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
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        print("Websocket:connection closed, close code={}".format(close_code))

    async def receive(self, text_data=None, bytes_data=None):
        print('Websocket:Receive message:{}'.format(text_data))
        await self.send(text_data=text_data)
