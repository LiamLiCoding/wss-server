import datetime
from django.db import models
from django.utils import timezone

# Create your models here.


class VerifyCode(models.Model):
    CODE_TYPE_CHOICE = (
        ('verify_email', 'verify_email'),
        ('reset_password', 'reset_password'),
    )

    code = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    code_type = models.CharField(max_length=20, choices=CODE_TYPE_CHOICE, default='verify_email')
    send_time = models.DateTimeField(default=timezone.now)
    expiration_time = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)

    class Meta:
        ordering = ["-send_time"]
        verbose_name = "verify_code"
        verbose_name_plural = "verify_code"


class SubscriptionEmail(models.Model):
    SUBSCRIPTION_TYPE_CHOICE = (
        ('new_function', 'New Function'),
    )

    email = models.EmailField(max_length=50)
    sub_type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPE_CHOICE, default='verify_email')
    sub_time = models.DateTimeField(default=timezone.now)
    is_activated = models.BooleanField(default=True)

    def __unicode__(self):
        return self.email

    class Meta:
        ordering = ["-sub_time"]
        verbose_name = "subscription_email"
        verbose_name_plural = "subscription_email"

