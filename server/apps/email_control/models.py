from django.db import models
from django.utils import timezone

# Create your models here.


class VerifyCode(models.Model):
    CONFIRM_TYPE_CHOICE = (
        ("register", "register"),
        ("forget", "forget_password")
    )
    code = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    send_type = models.CharField(max_length=20, choices=CONFIRM_TYPE_CHOICE)
    send_time = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)

    class Meta:
        ordering = ["-send_time"]
        verbose_name = "verify_code"
        verbose_name_plural = "verify_code"
