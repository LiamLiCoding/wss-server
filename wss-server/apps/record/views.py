from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import EventLog, OperationLog
from .pagination import LogPagination
from .serializers import EventLogSerializer, OperationLogSerializer


class GetLogByDeviceAPIView(LoginRequiredMixin, APIView):
	pagination = LogPagination()
	model = None
	serializer = None

	def get(self, request, device_id, *args, **kwargs):
		log_list = self.model.objects.filter(device=device_id)
		result = self.pagination.paginate_queryset(log_list, request)
		log_serializer = self.serializer(result, many=True)
		return self.pagination.get_paginated_response(log_serializer.data)


class GetLogByUserAPIView(LoginRequiredMixin, APIView):
	model = None
	serializer = None

	def get(self, request, *args, **kwargs):
		log_list = self.model.objects.filter(user=self.request.user)
		log_serializer = self.serializer(log_list, many=True)
		return Response(log_serializer.data)


class EventLogAPI(GetLogByDeviceAPIView):
	model = EventLog
	serializer = EventLogSerializer


class OperationLogAPI(GetLogByDeviceAPIView):
	model = OperationLog
	serializer = OperationLogSerializer


class GetEventLogByUserAPI(GetLogByUserAPIView):
	model = EventLog
	serializer = EventLogSerializer


class GetOperationLogByUserAPI(GetLogByUserAPIView):
	model = OperationLog
	serializer = OperationLogSerializer


