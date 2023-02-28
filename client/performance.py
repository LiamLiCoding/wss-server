#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/28 13:48
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu
import time

import psutil
import threading
import communicate

g_PERFORMANCE_MONITOR = None


def get_performance_monitor():
	global g_PERFORMANCE_MONITOR
	if not g_PERFORMANCE_MONITOR:
		g_PERFORMANCE_MONITOR = PerformanceMonitor()
	return g_PERFORMANCE_MONITOR


class PerformanceMonitor:
	def __init__(self):
		self.m_cpu_used_rate = 0
		self.m_mem_used_rate = 0
		self.m_mem_total = 0
		self.m_mem_swap_total = 0
		self.m_disk_io_read = 0
		self.m_disk_io_write = 0
		self.m_cpu_count = 0
		self.m_disk_usage = 0

		self.m_thread = None
		self.m_thread_lock = threading.Lock()
		self.m_event = None
		self.m_running = False
		self.m_enable_upload = True

	def get_static_info(self):
		self.m_cpu_count = psutil.cpu_count()
		self.m_disk_usage = psutil.disk_usage('/').percent
		self.m_mem_total = psutil.virtual_memory().total
		self.m_mem_swap_total = psutil.swap_memory().total
		return {'cpu_count': self.m_cpu_count,
		        'disk_usage': self.m_disk_usage,
		        'mem_total': self.m_mem_total,
		        'mem_swap_total': self.m_mem_swap_total}

	def get_dynamic_info(self):
		return {'cpu_used_rate': self.m_cpu_used_rate,
		        'mem_used_rate': self.m_mem_used_rate,
		        'disk_io_read': self.m_disk_io_read,
		        'disk_io_write': self.m_disk_io_write}

	def register_callback(self, event, func):
		pass

	def enable_upload(self, status):
		self.m_enable_upload = status

	def update_dynamic_info(self):
		if not self.m_running:
			self.stop()
			return

		with self.m_thread_lock:
			self.m_cpu_used_rate = psutil.cpu_percent(interval=1)
			self.m_mem_used_rate = psutil.virtual_memory().percent
			self.m_disk_io_read = psutil.disk_io_counters().read_bytes
			self.m_disk_io_write = psutil.disk_io_counters().write_bytes

			if self.m_enable_upload:
				communicate.websock_send(self.get_dynamic_info(), 'running_performance')
		if self.m_running:
			self.start()

	def start(self):
		self.m_running = True
		self.m_thread = threading.Timer(interval=1, function=self.update_dynamic_info)
		self.m_thread.start()

	def stop(self):
		self.m_running = False
		if self.m_thread:
			self.m_thread.cancel()
		self.m_thread = None

