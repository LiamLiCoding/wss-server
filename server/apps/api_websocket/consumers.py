#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/24 14:40
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

import json
from channels.generic.websocket import WebsocketConsumer


class DeviceConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print('888')
        self.send('123')

    def disconnect(self, close_code):
        print(9990)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print('1111', message)

        self.send(text_data=json.dumps({"message": message}))
        print(text_data)
