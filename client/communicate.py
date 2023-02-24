#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/24 16:00
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

import time
import threading
import websocket

websocket.enableTrace(True)
g_SERVER_CONNECT_OBJ = None


def init_server_connect_obj(url):
	global g_SERVER_CONNECT_OBJ
	if not g_SERVER_CONNECT_OBJ:
		g_SERVER_CONNECT_OBJ = ServerConnect(url)
	g_SERVER_CONNECT_OBJ.start()
	return g_SERVER_CONNECT_OBJ


def get_server_connect_obj():
	global g_SERVER_CONNECT_OBJ
	if not g_SERVER_CONNECT_OBJ:
		raise Exception('Please init server connect obj first')
	return g_SERVER_CONNECT_OBJ


class ServerConnect:
	def __init__(self, url):
		self.m_ws = None
		self.m_url = url
		self.m_thread = None
		self.m_running = False

	def _on_message(self, ws, message):
		print("message：%s" % message)

	def _on_error(self, ws, error):
		print("error", error)

	def _on_open(self, ws):
		print('connected')

	def _on_close(self, ws, close_status_code, close_msg):
		print('123', close_status_code)
		print(close_msg)

	def get_ws_obj(self):
		return self.m_ws

	def get_ws_thread(self):
		return self.m_thread

	def start(self):
		if self.m_running:
			print('Websocket cline is already running')
			return

		if not self.m_ws:
			self.m_running = True
			self.m_ws = websocket.WebSocketApp(url=self.m_url,
			                                   on_error=self._on_error,
			                                   on_open=self._on_open,
			                                   on_message=self._on_message,
			                                   on_close=self._on_close)
			# self.m_ws.run_forever()

			self.m_thread = threading.Thread(target=self.m_ws.run_forever)
			self.m_thread.daemon = True
			self.m_thread.start()

	def send(self, message):
		self.m_ws.send(message)


if __name__ == '__main__':
	# init_server_connect_obj("ws://127.0.0.1:8000/ws/chat/112/")
	init_server_connect_obj("ws://echo.websocket.events")
	ws = get_server_connect_obj()
	while True:
		time.sleep(1)
		input_msg = input("input your test:\n")
		ws.send(input_msg)

