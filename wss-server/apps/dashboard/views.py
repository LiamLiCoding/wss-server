from apps.accounts.mixins import UserSettingsMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.devices.models import Devices
from apps.record.models import EventLog


def redirect_to_dashboard(request):
    return redirect('/dashboard/')


class DashboardView(LoginRequiredMixin, UserSettingsMixin, TemplateView):
    template_name = "dashboard/dashboard-new.html"

    def get_events_and_devices_info(self):
        events_list = []
        devices_list = Devices.objects.filter(user=self.request.user)
        for device in devices_list:
            events = EventLog.objects.filter(device=device.id)
            if events:
                events_list.append(events)
        return devices_list, events_list

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        devices_list, events_list = self.get_events_and_devices_info()
        context.update({'devices_list': devices_list, 'events_list': events_list})
        context.update(self.get_user_info())
        if args:
            context.update(*args)
        return context


# TODO: tmp cancel dashboard page
def redirect_to_device(request):
    return redirect('/devices/')


class ComingSoonView(TemplateView):
    template_name = 'common/coming-soon.html'


def page_404(request, *args, **kwargs):
    return render(request, 'common/page-404.html')


def page_500(request, *args, **kwargs):
    return render(request, 'common/page-500.html')

