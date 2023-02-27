#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/24 14:40
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

from channels.generic.websocket import WebsocketConsumer


class DeviceConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print(self.scope)

    def disconnect(self, close_code):
        print("Websocket:connection closed, close code={}".format(close_code))

    def receive(self, text_data=None, bytes_data=None):
        print('Websocket:Receive message:{}'.format(text_data))
        self.send(text_data=text_data)
