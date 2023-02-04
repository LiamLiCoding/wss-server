#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/3 18:02
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu


import random
import string


def generate_digit_verification_code(digits=4):
	code_list = random.sample(string.digits, digits)
	result = ''
	for each_code in code_list:
		result += each_code
	return result


def generate_str_verification_code(digits=32):
	chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
	length = len(chars) - 1
	random_object = random.Random()
	results = ''
	for i in range(digits):
		results += chars[random_object.randint(0, length)]
	return results
