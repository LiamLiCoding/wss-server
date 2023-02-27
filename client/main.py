# WSS client
import time
import api_define
import websocket_client

API_KEY = 'pPrIkmvSP89JYo_xrGwPwbEVR6wRZO-cixisuDuGlDM'
ws_obj = websocket_client.init_websocket_client(api_define.WS_DEVICE_INFO_URL.format(api_key=API_KEY))

while True:
	time.sleep(1)
	input_msg = input("input your test:\n")
	ws_obj.send(input_msg)
