import json
import secrets
from django.conf import settings
from rest_framework import status
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.db.models import ObjectDoesNotExist
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from apps.accounts.mixins import UserSettingsMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, FileResponse, Http404

from .models import Devices, Performance
from apps.record.models import OperationLog
from apps.api_websocket.notification_consumer import send_notification
from apps.api_websocket.device_consumer import send_device_message
from apps.devices.serializers import PerformanceSerializer


class DeviceListView(LoginRequiredMixin, UserSettingsMixin, ListView):
    model = Devices
    template_name = "devices/devices_list.html"
    context_object_name = "devices"
    paginate_by = 5

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_info())
        activated_devices_num = 0
        active_devices_num = 0
        total_conversation = 0
        for each_object in context.get(self.context_object_name, []):
            if not each_object.is_enable:
                each_object.status = 'disable'
            else:
                if not each_object.is_activated:
                    each_object.status = 'inactivated'
                else:
                    activated_devices_num += 1
                    if each_object.is_active:
                        each_object.status = 'active'
                        active_devices_num += 1
                    else:
                        each_object.status = 'inactive'
            total_conversation += each_object.conversation_num

        context['activated_devices_num'] = activated_devices_num
        context['active_devices_num'] = active_devices_num
        context['total_conversation'] = total_conversation
        if args:
            context.update(*args)
        return context


class DeviceDetailView(LoginRequiredMixin, UserSettingsMixin, DetailView):
    model = Devices
    template_name = 'devices/device_detail.html'
    context_object_name = 'device'
    slug_field = 'id'
    slug_url_kwarg = 'device_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_info())
        return context


class DeleteDeviceView(LoginRequiredMixin, DeleteView):
    model = Devices
    success_url = reverse_lazy('devices_list')


class CreateDeviceView(LoginRequiredMixin, View):
    model = Devices
    template_name = "devices/devices_list.html"

    def post(self, request, *args, **kwargs):
        device_name = request.POST.get('device_name')
        node_type = request.POST.get('node_type')
        device_type = request.POST.get('device_type')
        protocol = request.POST.get('protocol')
        sdk = request.POST.get('sdk')
        if device_type and node_type and device_name and protocol and sdk:
            try:
                device = self.model.objects.get(name=device_name)
                if device:
                    render(request, self.template_name)
            except ObjectDoesNotExist:
                pass
            new_device = self.model()
            new_device.name = device_name
            new_device.node_type = node_type
            new_device.device_type = device_type
            new_device.protocol = protocol
            new_device.sdk = sdk
            new_device.user = request.user
            new_device.api_key = secrets.token_urlsafe(32)
            new_device.save()
            return redirect('/devices/')

        return redirect('/devices/')


class UpdateDeviceStatusView(LoginRequiredMixin, View):
    model = Devices
    template_name = "devices/devices_list.html"

    def post(self, request, *args, **kwargs):
        device_id = kwargs.get('pk')
        if device_id:
            try:
                device = self.model.objects.get(id=device_id)
                if device:
                    enable_status = request.POST.get("enable")
                    if enable_status:
                        device.is_enable = False if enable_status == 'false' else True
                    device.save()
                    return redirect(reverse('device_detail', kwargs={'device_id': device_id}))
            except ObjectDoesNotExist:
                pass
        return redirect('/devices/')


def download_sdk(request, sdk):
    if sdk == 'python':
        sdk_path = settings.BASE_DIR / 'media/devices/sdk/python_sdk.py'
        file_name = 'python_sdk.py'
    elif sdk == 'c++':
        sdk_path = settings.BASE_DIR / 'media/devices/sdk/cpp_sdk.cpp'
        file_name = 'cpp_sdk.cpp'
    else:
        return Http404

    file = open(sdk_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
    return response


class GetPerformanceDataAPI(LoginRequiredMixin, APIView):
    def get(self, request, device_id):
        try:
            device = Devices.objects.get(id=device_id)
            if device:
                performance = Performance.objects.filter(device=device)
                performance_serializer = PerformanceSerializer(performance, many=True)
                return Response(performance_serializer.data)
        except ObjectDoesNotExist:
            return Response(data=json.dumps({}), status=status.HTTP_404_NOT_FOUND)


class DeviceOperationAPI(LoginRequiredMixin, APIView):
    def post(self, request, device_id):
        try:
            device = Devices.objects.get(id=device_id)
            if device and device.is_active:
                operation = request.POST.get('operation')
                operation_type = request.POST.get('operation_type')
                ori_message = request.POST.get('message')

                message = 'Device {} {} {}, message: {}'.format(device.name, operation, operation_type, ori_message) \
                    if ori_message else 'Device {} {} {}'.format(device.name, operation, operation_type)

                send_device_message(device_id, {'operation': operation, 'operation_type': operation_type}, 'operation')

                operation_log = OperationLog()
                operation_log.operation = operation
                operation_log.operation_type = operation_type
                operation_log.device = device
                operation_log.message = message
                operation_log.save()
            else:
                send_notification(self.request.user.id, message='Operation failed. Device is offline', duration=5000,
                                  level='error', refresh=True, notification_type='swal')
            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(data=json.dumps({}), status=status.HTTP_404_NOT_FOUND)

