#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/28 19:18
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

from django.urls import path
from . import views

urlpatterns = [
	path('event-log-by-device/<int:device_id>', views.EventLogAPI.as_view(), name='get_event_log_by_device'),
	path('operation-log-by-device/<int:device_id>', views.OperationLogAPI.as_view(), name='get_operation_log_by_device'),
	path('event-log-by-user/<int:device_id>', views.EventLogAPI.as_view(), name='event_log_by_user'),
	path('operation-log-by-user/<int:device_id>', views.OperationLogAPI.as_view(), name='operation_log_by_user'),
]
