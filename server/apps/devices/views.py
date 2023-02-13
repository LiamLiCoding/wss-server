import secrets
from apps.accounts.mixins import UserSettingsMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import View
from django.db.models import ObjectDoesNotExist
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Devices


class DeviceListView(LoginRequiredMixin, UserSettingsMixin, ListView):
    model = Devices
    template_name = "devices/devices_list.html"
    context_obj_name = "devices"
    paginate_by = 6

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_info())
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
            return redirect('/devices/list')

        return redirect('/devices/list')


class UpdateDeviceView(LoginRequiredMixin, View):
    model = Devices
    template_name = "devices/devices_list.html"

    def post(self, request, *args, **kwargs):
        print(request)
        print(args)
        print(kwargs)
        return redirect('/devices/list')

