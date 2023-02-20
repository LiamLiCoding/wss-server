import requests
import time

from api_define import *


class BaseCommunicate:
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
        request = requests.post(GET_DEVICE_INFO, data=self.get_body_data())
        print(request.text)
        print(request.headers)
        return request.text


class UploadLog(BaseCommunicate):
    def upload_event_log(self):
        log_info = {
            'event': '1',
            'message': 'Detect motion'
        }
        data = self.get_body_data(log_info)
        request = requests.post(UPLOAD_EVENT_LOG, data=data)
        print(request.status_code)
        if request.status_code == 201:
            print("Upload log success")


if __name__ == '__main__':
    connection = BaseCommunicate('KUJ_zIZp2Qp5KpLl61-tWdl6zPvPbZmtEGrndhVRsVc')
    log_connection = UploadLog('KUJ_zIZp2Qp5KpLl61-tWdl6zPvPbZmtEGrndhVRsVc')
    connection.get_device_info()
    log_connection.upload_event_log()



