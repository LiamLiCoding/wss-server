"""wss_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.shortcuts import render
from django.conf.urls.static import static
from django.views.static import serve

from apps.dashboard import views as dashboard_views

urlpatterns = [
    path('', dashboard_views.redirect_to_dashboard),
    path('dashboard/', include('apps.dashboard.urls')),
    path('api-control/', include('apps.api_control.urls')),
    path('email/', include('apps.email.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('devices/', include('apps.devices.urls')),
    path('record/', include('apps.record.urls')),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def handler_404_page(request, exception=None):
    return render(request, 'common/page-404.html')


def handler_500_page(request, *args, **kwargs):
    return render(request, 'common/page-500.html')


handler404 = handler_404_page
handler500 = handler_500_page