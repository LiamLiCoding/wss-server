#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/24 13:57
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

# chat/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]