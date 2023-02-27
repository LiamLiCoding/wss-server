import requests
import time
import http_status_code

from api_define import *


class HttpClient:
    def __init__(self, device_key):
        self.m_device_key = device_key

    @staticmethod
    def get_timestamp():
        millis = int(round(time.time() * 1000))
        return millis

    def get_body_data(self, data=None):
        timestamp = self.get_timestamp()
        body = {
            'timestamp': timestamp,
            'device_key': self.m_device_key
        }
        if data:
            body.update(data)
        return body

    def get_device_info(self):
        request = requests.post(HTTP_GET_DEVICE_INFO, data=self.get_body_data())
        return request.text

    def upload_event_log(self, event, message):
        log_info = {
            'event': event,
            'message': message
        }
        data = self.get_body_data(log_info)
        request = requests.post(HTTP_UPLOAD_EVENT_LOG, data=data)
        if request.status_code != http_status_code.HTTP_201_CREATED:
            print("Upload log failed")


if __name__ == '__main__':
    connection = HttpClient('KUJ_zIZp2Qp5KpLl61-tWdl6zPvPbZmtEGrndhVRsVc')
    connection.get_device_info()
    connection.upload_event_log('1', 'test')



