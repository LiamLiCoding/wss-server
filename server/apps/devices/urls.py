#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/4 3:09
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu


from django.urls import path
from . import views

urlpatterns = [
	path('', views.DeviceListView.as_view(), name='devices_list'),
	path('create/', views.CreateDeviceView.as_view(), name='create_device'),
	path('detail/<int:device_id>', views.DeviceDetailView.as_view(), name='device_detail'),
	path('delete/<pk>', views.DeleteDeviceView.as_view(), name='delete_device'),
	path('update/<pk>', views.UpdateDeviceStatusView.as_view(), name='update_device_status'),
	path('edit_device/<pk>', views.UpdateDeviceStatusView.as_view(), name='edit_device'),
	path('download_sdk/<str:sdk>', views.download_sdk, name='download_sdk'),
	path('get_performance/<int:device_id>', views.GetPerformanceDataAPI.as_view(), name='get_performance'),
	path('operation/<int:device_id>', views.DeviceOperationAPI.as_view(), name='operation'),
]
