from django.shortcuts import render

from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = "dashboard/dashboard.html"


def page_404(request, *args, **kwargs):
    return render(request, 'common/page-404.html')


def page_500(request, *args, **kwargs):
    return render(request, 'common/page-500.html')

