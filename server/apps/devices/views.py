from apps.accounts.mixins import UserSettingsMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class DeviceListView(LoginRequiredMixin, UserSettingsMixin, TemplateView):
    template_name = "devices/devices_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_info())
        if args:
            context.update(*args)
        return context
