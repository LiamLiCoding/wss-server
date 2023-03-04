#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/24 14:40
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/device/<str:api_key>", consumers.DeviceConsumer.as_asgi()),
    path("ws/notification/", consumers.NotificationConsumer.as_asgi()),
]
