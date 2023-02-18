from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from django.db.models import ObjectDoesNotExist

from apps.devices.models import Devices
from apps.devices.serializers import DevicesSerializer


@api_view(['GET', 'POST'])
def activate_device(request):
    if request.method == 'GET':
        device = Devices.objects.all()
        return Response({})

    elif request.method == 'POST':
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class DeviceInfoView(APIView):
    def post(self, request, key):
        print(request)
        print(request.META)
        print(request.META.keys())
        print(type(request))
        try:
            device = Devices.objects.get(api_key=key)
            if device:
                device_serializer = DevicesSerializer(device)
                return Response(device_serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_404_NOT_FOUND)


class GetTokenView(APIView):
    def post(self, request):
        print(request)
        print(request.META)
        print(request.META.keys())
        return Response({'status': 'success'})

