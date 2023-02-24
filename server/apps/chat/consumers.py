# chat/consumers.py
import json
import threading
import time

from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        def run():
            time.sleep(2)
            self.send('123')
        self.accept()
        self.send('Server ws connected')
        print('Server ws connected')
        threading



    def disconnect(self, close_code):
        print("server: ws disconnected")
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print(112, message)

        self.send(text_data=json.dumps({"message": message}))

