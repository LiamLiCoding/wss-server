import secrets
from django.views.generic import View
from django.http import JsonResponse
from apps.accounts.mixins import UserSettingsMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.db.models import ObjectDoesNotExist
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse


from .models import Devices


class DeviceListView(LoginRequiredMixin, UserSettingsMixin, ListView):
    model = Devices
    template_name = "devices/devices_list.html"
    context_object_name = "devices"
    paginate_by = 6

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
            total_conversation += each_object.suc_conv_num

        context['activated_devices_num'] = activated_devices_num
        context['active_devices_num'] = active_devices_num
        context['total_conversation'] = total_conversation
        if args:
            context.update(*args)
        return context


class DeviceDetailView(DetailView):
    model = Devices
    template_name = 'devices/device_detail.html'
    context_object_name = 'device'
    slug_field = 'id'
    slug_url_kwarg = 'device_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
                device = self.model.objects.get(device_name=device_name)
                if device:
                    render(request, self.template_name)
            except ObjectDoesNotExist:
                pass
            new_device = self.model()
            new_device.device_name = device_name
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

                    # get status
                    if not device.is_enable:
                        status = 'disable'
                    else:
                        if not device.is_activated:
                            status = 'inactivated'
                        else:
                            if device.is_active:
                                status = 'active'
                            else:
                                status = 'inactive'

                    response = {
                        'target_id': device.id,
                        'is_enable': device.is_enable,
                        'device_status': status,
                    }
                    return JsonResponse(response)
            except ObjectDoesNotExist:
                pass
        return redirect('/devices/')

