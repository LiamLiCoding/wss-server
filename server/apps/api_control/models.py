import secrets
import datetime

from django.db import models
from django.utils import timezone


class APIKeyManager(models.Manager):

    def create_key(self, **kwargs):
        obj = self.model(**kwargs)
        key = secrets.token_urlsafe(16)
        obj.key = key
        obj.expiration_date = (timezone.now() + datetime.timedelta(days=30))
        obj.save()
        return obj

    def is_valid(self, key: str) -> bool:
        try:
            api_key = self.get(key=key)
        except self.model.DoesNotExist:
            return False

        if api_key.expiration_time.created_time < timezone.now():
            return False

        return True


class APIKey(models.Model):
    STATUS_CHOICES = (
        ('expired', 'Expired'),
        ('disable', 'Disable'),
        ('enable', 'Enable'),
    )

    objects = APIKeyManager()
    key = models.CharField(max_length=150, editable=False)
    name = models.CharField(max_length=200, blank=False, default=None)
    owner = models.CharField(max_length=50, blank=False, default=None)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='enable')
    created_time = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        ordering = ("-created_time",)
        verbose_name = "API key"
        verbose_name_plural = "API keys"

    def __str__(self) -> str:
        return str(self.name)

