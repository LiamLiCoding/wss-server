import time
from rest_framework import serializers
from cffi.backend_ctypes import long

from .models import Devices, Performance


class DevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devices
        fields = ['device_name', 'node_type', 'device_type', 'protocol', 'sdk']


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        created_time = data.get('created_time')
        created_time_stamp = time.mktime(time.strptime(created_time, '%Y-%m-%dT%H:%M:%S.%fZ'))
        data.update({"created_time": int(created_time_stamp) * 1000})
        return data
