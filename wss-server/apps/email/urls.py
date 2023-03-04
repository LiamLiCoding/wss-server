#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/3 19:48
# @Author : Haozheng Li (Liam)
# @Email : haozheng.l@outlook.com

from django.urls import path
from . import views

urlpatterns = [
	path('email_verify/<str:request_email>', views.EmailVerify.as_view(), name='email_verify'),
	path('resend_email_verify/<str:request_email>', views.ResendEmailVerify.as_view(), name='resend_email_verify'),
	path('email_verify_success/', views.EmailVerifySuccessView.as_view(), name='email_verify_success'),
	path('forget_password/', views.ForgetPasswordView.as_view(), name='forget_password'),
	path('reset_link_sent/', views.ResetLinkSentView.as_view(), name='reset_link_sent'),
]

