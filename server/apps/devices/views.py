import secrets
from apps.accounts.mixins import UserSettingsMixin
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import View
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


class CreateDeviceView(LoginRequiredMixin, View):
    model = Devices

    def get_success_url(self):
        return reverse('devices_list')

