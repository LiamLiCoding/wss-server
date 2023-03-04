from django.contrib import admin

# Register your models here.

from .models import APIKey

admin.site.register(APIKey)
