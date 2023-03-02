#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/28 19:18
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

from django.urls import path
from . import views

urlpatterns = [
	path('event-log/<int:device_id>', views.EventLogAPI.as_view(), name='event_log'),
	path('operation-log/<int:device_id>', views.OperationLogAPI.as_view(), name='operation_log'),
]
