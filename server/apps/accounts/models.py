from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Users(AbstractUser):
    create_time = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='accounts/avatar', max_length=200, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-create_time"]
        verbose_name = "user"
        verbose_name_plural = "users"



