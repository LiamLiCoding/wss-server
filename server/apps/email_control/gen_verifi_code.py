#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/3 18:02
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu


import random
import string


def generate_digit_verification_code(digits=4):
	return random.sample(string.digits, digits)
