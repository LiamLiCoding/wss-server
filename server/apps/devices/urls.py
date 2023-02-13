#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/4 3:09
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu


from django.urls import path
from . import views

urlpatterns = [
	path('list/', views.DeviceListView.as_view(), name='devices_list'),
	path('create/', views.CreateDeviceView.as_view(), name='create_device'),
]
