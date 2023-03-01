#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/28 22:46
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu


from rest_framework.pagination import PageNumberPagination


class LogPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'size'
    max_page_size = 10
