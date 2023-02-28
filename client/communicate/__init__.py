#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/27 17:32
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

from . import websocket_client
from .api_define import *


def init_websocket_client(url):
	return websocket_client.init_websocket_client(url)


def get_websocket_client():
	return websocket_client.get_websocket_client()


def websock_send(message, message_type):
	websocket_client.get_websocket_client().send(message, message_type)
