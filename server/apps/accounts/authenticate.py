#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/1/27 16:09
# @Author : Haozheng Li (Liam)
# @Email : haozheng.l@outlook.com

from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q, ObjectDoesNotExist

from .models import Users


class LoginBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Users.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except ObjectDoesNotExist as error:
            return error
