import datetime
from apps.accounts.mixins import UserSettingsMixin
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.devices.models import Devices
from apps.record.models import EventLog, OperationLog


def redirect_to_dashboard(request):
    return redirect('/dashboard/')


class DashboardView(LoginRequiredMixin, UserSettingsMixin, TemplateView):
    template_name = "dashboard/dashboard-new.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        devices_list = Devices.objects.filter(user=self.request.user)
        online_devices_num = len(devices_list.filter(is_active=True))
        total_conversation = sum([device.conversation_num for device in devices_list])
        total_event_logs_list = EventLog.objects.filter(user=self.request.user)
        total_operation_logs_list = OperationLog.objects.filter(user=self.request.user)
        today_event_num = len(total_event_logs_list.filter(created_time__startswith=datetime.date.today()))
        today_operation_num = len(total_operation_logs_list.filter(created_time__startswith=datetime.date.today()))
        latest_event_log = total_event_logs_list.order_by('-created_time')[0] if total_event_logs_list else 0
        context.update({'devices_list': devices_list,
                        'online_devices_num': online_devices_num,
                        'total_conversation': total_conversation,
                        'events_list': total_event_logs_list,
                        'operations_list': total_operation_logs_list,
                        'today_events': today_event_num, 'today_operations': today_operation_num,
                        'latest_event': latest_event_log})
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

