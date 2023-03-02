import json
import threading
import time

import websocket

websocket.enableTrace(True)	 # Only on development env
g_WEBSOCKET_CLIENT = None


def init_websocket_client(url):
	global g_WEBSOCKET_CLIENT
	if not g_WEBSOCKET_CLIENT:
		g_WEBSOCKET_CLIENT = WebsocketClient(url)
	g_WEBSOCKET_CLIENT.start()
	return g_WEBSOCKET_CLIENT


def get_websocket_client():
	global g_WEBSOCKET_CLIENT
	if not g_WEBSOCKET_CLIENT:
		raise RuntimeError('Please init server connect obj first')
	return g_WEBSOCKET_CLIENT


class WebsocketClient:
	def __init__(self, url):
		self.m_ws = None
		self.m_url = url
		self.m_thread = None
		self.m_connected = False
		self.m_thread_lock = threading.Lock()

	def get_ws_obj(self):
		return self.m_ws

	def on_message(self, ws_obj, message):
		self.m_connected = True
		print("Websocket client: received message：{}".format(message))

	def on_error(self, ws_obj, error):
		self.m_connected = False
		if isinstance(error, ConnectionRefusedError) or isinstance(error, websocket.WebSocketConnectionClosedException):
			print("Websocket client - Connection Error:{}".format(error))
		else:
			print("Websocket client - Other Error:{}".format(error))

	def on_open(self, ws_obj):
		self.m_connected = True
		print('Websocket client: Successfully connected!')

	def on_close(self, ws_obj, close_status_code, close_msg):
		self.m_connected = False
		self.reconnect()
		print('Websocket client: Connection closed, close code:{}, close message:{}'.format(close_status_code, close_msg))

	def stop(self):
		self.m_ws.close()
		if self.m_thread:
			self.m_thread.join()
			self.m_thread = None

	def start(self):
		self.m_ws = websocket.WebSocketApp(
			url=self.m_url,
			on_error=self.on_error,
			on_open=self.on_open,
			on_message=self.on_message,
			on_close=self.on_close)

		self.m_thread = threading.Thread(target=self.m_ws.run_forever)
		self.m_thread.daemon = True
		self.m_thread.start()

	def send(self, message, message_type):
		data = {'message': message,
		        'message_type': message_type}
		if self.m_connected:
			try:
				self.m_ws.send(json.dumps(data))
			except websocket.WebSocketConnectionClosedException as error:
				print('Websocket send messages failed, error:{}'.format(error))

	def reconnect(self):
		self.m_ws.close()
		time.sleep(5)
		print("Websocket client - reconnect ...")
		self.start()


