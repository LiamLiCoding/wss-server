#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/1 16:01
# @Author : Haozheng Li (Liam)
# @Email : haozheng.l@outlook.com


from django.urls import path
from . import views

urlpatterns = [
	path('', views.ApiKeysView.as_view(), name='api-key'),
	path('create-api-key/', views.CreateApiKeyView.as_view(), name='create-api-key'),
	path('delete-api-key/<pk>', views.DeleteApiKeyView.as_view(), name='delete-api-key'),
]
