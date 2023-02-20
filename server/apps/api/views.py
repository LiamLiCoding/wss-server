import datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import ObjectDoesNotExist
from django.utils import timezone
from apps.devices.models import Devices
from apps.record.models import SurveillanceLog
from apps.devices.serializers import DevicesSerializer


class DeviceInfoMixin:
    def get_device_data(self, device_key):
        try:
            device = Devices.objects.get(api_key=device_key)
            if device and device.is_enable:
                device_serializer = DevicesSerializer(device)
                return device, device_serializer.data
        except ObjectDoesNotExist:
            pass
        return None, {}


class GetDeviceInfoView(APIView, DeviceInfoMixin):
    def post(self, request):
        device_key = request.POST.get('device_key')
        device, device_data = self.get_device_data(device_key)
        if device:
            device.is_activated = True
            device.is_active = True
            device.last_online = timezone.now()
            device.save()
            return Response(device_data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SurveillanceLogView(APIView, DeviceInfoMixin):
    def post(self, request):
        device_key = request.POST.get('device_key')
        event = request.POST.get('event')
        message = request.POST.get('message')
        device, device_data = self.get_device_data(device_key)
        if device_data:
            new_log = SurveillanceLog(message=message, event=event, device=device)
            new_log.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
