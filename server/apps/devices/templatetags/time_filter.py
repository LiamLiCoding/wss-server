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
    hours = int(time_delta.seconds / 3600)
    minutes = int((time_delta.seconds - hours * 3600) / 60)
    return "{} hour {} min".format(hours, minutes)


