from django.db import models

from apps.accounts.models import Users


class Notification(models.Model):
    STATUS_CHOICE = (
        ('unread', 'unread'),
        ('have_read', 'have_read'),
    )
    TYPE_CHOICE = (
        ('message', 'message'),
        ('alert', 'alert'),
    )

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default='unread')
    type = models.CharField(max_length=50, choices=TYPE_CHOICE, default='message')
    message = models.TextField(null=True, default=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_time",)
        verbose_name = "notification"
        verbose_name_plural = "notification"

    def __str__(self) -> str:
        return str(self.type)

