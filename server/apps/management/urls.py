#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/1/31 14:44
# @Author : Haozheng Li (Liam)
# @Email : haozheng.l@outlook.com

from django.urls import path

from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
