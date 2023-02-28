#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/27 22:23
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

import datetime
from django import template
from django.utils import timezone

register = template.Library()


@register.filter(is_safe=True)
def time_diff_now(value):
    time_delta = timezone.now() - value
    return "{} day {} min".format(int(time_delta.seconds / 3600), int(time_delta.seconds / 60))


