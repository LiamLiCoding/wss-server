from django.db import models
from apps.devices.models import Devices


class EventLog(models.Model):
    EVENT_TYPE = (
        (1, 'Event1'),
        (2, 'Event2'),
        (3, 'Event3'),
        (4, 'Event4'),
    )

    device = models.ForeignKey(Devices, on_delete=models.CASCADE)
    event = models.IntegerField(choices=EVENT_TYPE, default=1)
    message = models.TextField(null=True, blank=True)
    action = models.TextField(null=True, blank=True)
    image_url = models.FileField(upload_to='devices/log_img', null=True, blank=True, default='devices/log_img/test.jpg')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_time",)
        verbose_name = "eventlog"
        verbose_name_plural = "eventlog"

    def __str__(self) -> str:
        return str(self.event)


class OperationLog(models.Model):
    OPERATION_TYPE = (
        ('Shutdown', 'Shutdown'),
        ('Restart', 'Restart'),
        ('Other', 'Other'),
    )

    device = models.ForeignKey(Devices, on_delete=models.CASCADE)
    operation = models.CharField(max_length=50, choices=OPERATION_TYPE, default='1')
    message = models.TextField(null=True, default=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_time",)
        verbose_name = "operation_log"
        verbose_name_plural = "operation_log"

    def __str__(self) -> str:
        return str(self.operation)
