#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/1 16:01
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu


from django.urls import path
from . import views

urlpatterns = [
	path('', views.DashboardView.as_view(), name='dashboard'),
]
