from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models import Q


class Users(AbstractUser):
    USER_SOURCE_CHOICE = (
        ("blog", "Blog"),
        ("github", "Github"),
    )

    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-create_time"]
        verbose_name = "users"
        verbose_name_plural = "users"


class Profile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='accounts/avatar', max_length=200, null=True, blank=True)
    oauth_id = models.PositiveIntegerField('Oauth-id', unique=True, null=True, blank=True)
    oauth_page_url = models.CharField('Oauth-Page-Url', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username


