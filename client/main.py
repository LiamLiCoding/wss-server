# WSS client
import time
import communicate

API_KEY = 'ruAQRFEM5xBhilAPrFE1J3PxcnKQ4XIlwFlY1MQWolk'
ws_obj = communicate.init_websocket_client(communicate.WS_DEVICE_INFO_URL.format(api_key=API_KEY))

while True:
	time.sleep(1)
	input_msg = input("input your test:\n")
	ws_obj.send(input_msg)
