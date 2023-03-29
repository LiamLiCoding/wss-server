from django.db import models
from apps.accounts.models import Users


class Devices(models.Model):
    NODE_TYPE_CHOICES = (
        ('IntruderDetect', 'IntruderDetect'),
        ('Gateway', 'Gateway'),
    )
    DEVICE_TYPE_CHOICES = (
        ('RaspberryPi', 'Raspberry Pi'),
    )
    PROTOCOL_CHOICES = (
        ('Websocket', 'Websocket'),
    )

    name = models.CharField(max_length=200, blank=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    node_type = models.CharField(max_length=200, choices=NODE_TYPE_CHOICES, default='motion IntruderDetect')
    device_type = models.CharField(max_length=200, choices=DEVICE_TYPE_CHOICES, default='RaspberryPi')
    api_key = models.CharField(max_length=150, editable=False, blank=False, null=False)

    is_activated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_enable = models.BooleanField(default=True)

    protocol = models.CharField(max_length=50, choices=PROTOCOL_CHOICES, default='Websocket')
    conversation_num = models.PositiveIntegerField(default=0)

    created_time = models.DateTimeField(auto_now_add=True)
    last_online = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("-created_time",)
        verbose_name = "devices"
        verbose_name_plural = "devices"

    def __str__(self) -> str:
        return str(self.name)


class Performance(models.Model):
    device = models.ForeignKey(Devices, on_delete=models.CASCADE)
    cpu_rate = models.DecimalField(max_digits=5, decimal_places=1)
    mem_rate = models.DecimalField(max_digits=5, decimal_places=1)
    disk_write_io = models.BigIntegerField(default=0)
    disk_read_io = models.BigIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_time",)
        verbose_name = "performance"
        verbose_name_plural = "performance"

    def __str__(self) -> str:
        return str(self.device)

