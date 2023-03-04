#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/4 2:25
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu


class UserSettingsMixin:
	def get_user_info(self):
		user = self.request.user
		context = {}
		if user:
			context['username'] = user.username
			context['avatar'] = user.avatar
			context['first_name'] = user.first_name
			context['last_name'] = user.last_name
			context['email'] = user.email
			context['is_staff'] = user.is_staff
		return context
