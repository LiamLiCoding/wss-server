#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/3 19:48
# @Author : Haozheng Li (Liam)
# @Email : haozheng.l@outlook.com

from django.urls import path
from . import views

urlpatterns = [
	path('email_verify/<str:request_email>', views.TwoStepVerifyView.as_view(), name='email_verify'),
]

