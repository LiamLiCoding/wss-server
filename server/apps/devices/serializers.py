import time
from rest_framework import serializers

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
        disk_write_io = data.get('disk_write_io')
        disk_read_io = data.get('disk_read_io')
        created_time_stamp = time.mktime(time.strptime(created_time, '%Y-%m-%dT%H:%M:%S.%fZ'))
        data.update({"created_time": int(created_time_stamp) * 1000})
        data.update({"disk_write_io": int(disk_write_io / 1000)})
        data.update({"disk_read_io": int(disk_read_io / 1000)})
        return data
