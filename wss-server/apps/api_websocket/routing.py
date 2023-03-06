#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/24 14:40
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

from django.urls import path

from .notification_consumer import NotificationConsumer
from .device_consumer import DeviceConsumer

websocket_urlpatterns = [
    path("ws/device/<str:api_key>", DeviceConsumer.as_asgi()),
    path("ws/notification/", NotificationConsumer.as_asgi()),
]
