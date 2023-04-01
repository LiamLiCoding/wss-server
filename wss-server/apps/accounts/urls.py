#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2022/12/27 16:47
# @Author : Haozheng Li (Liam)
# @Email : haozheng.l@outlook.com

from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_login),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('settings/', views.AccountSettings.as_view(), name='account_settings'),
    path('settings/change_personal_info/', views.ChangePersonalInfoAPI.as_view(), name='change_personal_info'),
    path('settings/change_password/', views.ChangePasswordAPI.as_view(), name='change_password'),
    path('oauth/github/', views.GitHubOAuthView.as_view(), name='github_oauth'),
    path('reset_password/<str:code>/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('reset_password_success/', views.ResetPasswordSuccessView.as_view(), name='reset_password_success'),
    path('email_verify/<str:request_email>', views.EmailVerify.as_view(), name='email_verify'),
    path('resend_email_verify/<str:request_email>', views.ResendEmailVerify.as_view(), name='resend_email_verify'),
    path('email_verify_success/', views.EmailVerifySuccessView.as_view(), name='email_verify_success'),
    path('forget_password/', views.ForgetPasswordView.as_view(), name='forget_password'),
    path('reset_link_sent/', views.ResetLinkSentView.as_view(), name='reset_link_sent'),
]
