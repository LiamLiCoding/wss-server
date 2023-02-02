from django.shortcuts import render
from django.views.generic import TemplateView


class ApiKeysView(TemplateView):
    template_name = "api_control/api-keys.html"
