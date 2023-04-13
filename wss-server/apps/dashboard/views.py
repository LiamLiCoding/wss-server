import datetime
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import TruncDate
from django.db.models import Count, ObjectDoesNotExist

from django.shortcuts import redirect
from django.views.generic import TemplateView
from apps.accounts.mixins import UserSettingsMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.devices.models import Devices
from apps.system.models import SystemSetting
from apps.accounts.models import LoginHistory
from apps.record.models import EventLog, OperationLog


def redirect_to_dashboard(request):
    return redirect('/dashboard/')


class DashboardView(LoginRequiredMixin, UserSettingsMixin, TemplateView):
    template_name = "dashboard/dashboard-new.html"

    def get_system_settings(self):
        try:
            system_settings = SystemSetting.objects.get(user=self.request.user)
            if system_settings:
                return system_settings
        except ObjectDoesNotExist:
            pass
        except Exception as ee:
            print('system settings create error: {}'.format(ee))
        system_settings = SystemSetting()
        system_settings.user = self.request.user
        system_settings.save()

        return system_settings

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        devices_list = Devices.objects.filter(user=self.request.user)
        system_settings = self.get_system_settings()
        online_devices_num = len(devices_list.filter(is_active=True))
        total_conversation = sum([device.conversation_num for device in devices_list])
        total_event_logs_list = EventLog.objects.filter(user=self.request.user)
        recent_events_logs_list = EventLog.objects.filter(user=self.request.user).order_by('-id')[:5]
        total_operation_logs_list = OperationLog.objects.filter(user=self.request.user)
        today_event_num = len(total_event_logs_list.filter(created_time__startswith=datetime.date.today()))
        today_operation_num = len(total_operation_logs_list.filter(created_time__startswith=datetime.date.today()))
        latest_event_log = total_event_logs_list.order_by('-created_time')[0] if total_event_logs_list else 0

        context.update({'devices_list': devices_list,
                        'online_devices_num': online_devices_num,
                        'total_conversation': total_conversation,
                        'events_list': total_event_logs_list,
                        'operations_list': total_operation_logs_list,
                        'today_events': today_event_num,
                        'recent_events': recent_events_logs_list,
                        'today_operations': today_operation_num,
                        'latest_event': latest_event_log})

        login_history = LoginHistory.objects.filter(user=self.request.user)
        context.update({'login_history': login_history})
        context.update({'system_settings': system_settings})

        context.update(self.get_user_info())
        if args:
            context.update(*args)
        return context


class LogChartDataAPI(APIView):
    def get(self, request, *args, **kwargs):
        one_month_ago = timezone.now() - timedelta(days=30)
        daily_events = (
            EventLog.objects
                .filter(created_time__gte=one_month_ago)
                .annotate(x=TruncDate('created_time'))
                .values('created_time')
                .annotate(y=Count('id'))
                .order_by('created_time')
        )
        for each in daily_events:
            each.update({'x': each['created_time']})

        daily_operations = (
            OperationLog.objects
                .filter(created_time__gte=one_month_ago)
                .annotate(x=TruncDate('created_time'))
                .values('created_time')
                .annotate(y=Count('id'))
                .order_by('created_time')
        )
        for each in daily_operations:
            each.update({'x': each['created_time']})

        return Response(data={'events': daily_events, 'operations': daily_operations})

