from datetime import datetime
from rest_framework import serializers
from .models import EventLog, OperationLog


class EventLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLog
        fields = '__all__'


class OperationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationLog
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        created_time = data.get('created_time')
        created_time = datetime.fromisoformat(created_time).strftime('%b.%d, %Y %H:%M:%S')
        data.update({"created_time": created_time})
        return data
