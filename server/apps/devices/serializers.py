from rest_framework import serializers

from .models import Devices


class DevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devices
        fields = ['device_name', 'node_type', 'device_type', 'protocol', 'sdk']
