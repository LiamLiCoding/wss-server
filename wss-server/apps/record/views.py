from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import EventLog, OperationLog
from .pagination import LogPagination
from .serializers import EventLogSerializer, OperationLogSerializer


class EventLogAPI(LoginRequiredMixin, APIView):
	def get(self, request, device_id, *args, **kwargs):
		page = LogPagination()
		log_list = EventLog.objects.filter(device=device_id)
		result = page.paginate_queryset(log_list, request)
		event_log_serializer = EventLogSerializer(result, many=True)
		return page.get_paginated_response(event_log_serializer.data)


class OperationLogAPI(LoginRequiredMixin, APIView):
	def get(self, request, device_id):
		page = LogPagination()
		log_list = OperationLog.objects.filter(device=device_id)
		result = page.paginate_queryset(log_list, request)
		operation_log_serializer = OperationLogSerializer(result, many=True)
		return page.get_paginated_response(operation_log_serializer.data)
