from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('activate/', views.activate_device, name='activate_device'),
    path('device-info/', views.DeviceInfoView.as_view()),
    path('get-token/', views.GetTokenView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
