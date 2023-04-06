#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/4/6 15:38
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

from django.shortcuts import render


def handler_404_page(request, exception=None):
    return render(request, 'common/page-404.html')


def handler_500_page(request, *args, **kwargs):
    return render(request, 'common/page-500.html')


def maintenance(request, *args, **kwargs):
    return render(request, 'common/maintenance.html')


def coming_soon_page(request, *args, **kwargs):
    return render(request, 'common/coming-soon.html')