from django.db import models
from apps.devices.models import Devices


class SurveillanceLog(models.Model):
    EVENT_TYPE = (
        ('1', 'Event1'),
        ('2', 'Event2'),
        ('3', 'Event3'),
        ('4', 'Event4'),
    )

    device = models.ForeignKey(Devices, on_delete=models.CASCADE)
    event = models.CharField(max_length=50, choices=EVENT_TYPE, default='1')
    message = models.TextField(null=True, default=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_time",)
        verbose_name = "SurveillanceLog"
        verbose_name_plural = "SurveillanceLog"

    def __str__(self) -> str:
        return str(self.device)
