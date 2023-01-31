#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2022/12/27 16:47
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_login),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.LoginView.as_view(), name='register'),
]
