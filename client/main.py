# WSS client
import time
import communicate
import performance

API_KEY = 'ruAQRFEM5xBhilAPrFE1J3PxcnKQ4XIlwFlY1MQWolk'

ws_obj = communicate.init_websocket_client(communicate.WS_DEVICE_INFO_URL.format(api_key=API_KEY))
monitor = performance.get_performance_monitor()
monitor.start()

while True:
	time.sleep(1)
