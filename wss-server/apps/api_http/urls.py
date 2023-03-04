#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/24 12:36
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('device-info/', views.GetDeviceInfoView.as_view()),
    path('surveillance-log/', views.EventLogView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
