import secrets
import datetime

from django.db import models
from apps.accounts.models import Users
from django.utils import timezone


class APIKey(models.Model):
    STATUS_CHOICES = (
        ('expired', 'Expired'),
        ('disable', 'Disable'),
        ('enable', 'Enable'),
    )

    key = models.CharField(max_length=150)
    name = models.CharField(max_length=200, blank=False, default=None)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='enable')
    created_time = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(blank=True, null=True, default=timezone.now() + datetime.timedelta(days=180))

    class Meta:
        ordering = ("-created_time",)
        verbose_name = "API key"
        verbose_name_plural = "API keys"

    def __str__(self) -> str:
        return str(self.name)



