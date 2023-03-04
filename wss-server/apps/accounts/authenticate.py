#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/1/27 16:09
# @Author : Haozheng Li (Liam)
# @Email : haozheng.l@outlook.com

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q, ObjectDoesNotExist

from .models import Users


class LoginBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return
        try:
            user = Users.objects.get(email=email)
            if user.check_password(password):
                return user
        except ObjectDoesNotExist as error:
            return error
