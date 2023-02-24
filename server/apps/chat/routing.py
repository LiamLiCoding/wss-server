#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/24 14:07
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]