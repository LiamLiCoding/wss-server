from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import ObjectDoesNotExist

from apps.devices.models import Devices
from apps.devices.serializers import DevicesSerializer


class DeviceInfoMixin:
    def get_device_data(self, device_key):
        print("!!!!")
        print(Devices.objects.all[0].api_key)
        try:
            device = Devices.objects.get(api_key=device_key)
            if device:
                device_serializer = DevicesSerializer(device)
                return device_serializer.data
        except ObjectDoesNotExist:
            return {}


class DeviceInfoView(APIView, DeviceInfoMixin):
    def post(self, request):
        print("#####")
        device_key = request.POST.get('device_key')
        device_data = self.get_device_data(device_key)
        if device_data:
            return Response(device_data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)