from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('device-info/', views.DeviceInfoView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
