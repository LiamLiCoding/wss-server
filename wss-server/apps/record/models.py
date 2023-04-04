from django.db import models
from apps.devices.models import Devices
from apps.accounts.models import Users


class EventLog(models.Model):
    EVENT_TYPE = (
        (1, 'Event1'),
        (2, 'Event2'),
        (3, 'Event3'),
        (4, 'Event4'),
    )
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    device = models.ForeignKey(Devices, on_delete=models.CASCADE)
    event = models.IntegerField(choices=EVENT_TYPE, default=1)
    message = models.TextField(null=True, blank=True)
    action = models.TextField(null=True, blank=True)
    resource_url = models.FileField(upload_to='devices/log_img', null=True, blank=True, default='devices/log_img/test.jpg')
    resource_type = models.CharField(max_length=50, default='image')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_time",)
        verbose_name = "eventlog"
        verbose_name_plural = "eventlog"

    def __str__(self) -> str:
        return str(self.event)


class OperationLog(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    device = models.ForeignKey(Devices, on_delete=models.CASCADE)
    operation = models.CharField(max_length=50)
    operation_type = models.CharField(max_length=50)
    message = models.TextField(null=True, default=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_time",)
        verbose_name = "operation_log"
        verbose_name_plural = "operation_log"

    def __str__(self) -> str:
        return str(self.operation)
