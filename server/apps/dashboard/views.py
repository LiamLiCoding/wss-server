from apps.accounts.mixins import UserSettingsMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


def redirect_to_dashboard(request):
    return redirect('/dashboard/')


class DashboardView(LoginRequiredMixin, UserSettingsMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_info())
        if args:
            context.update(*args)
        return context


# TODO: tmp cancel dashboard page
def redirect_to_device(request):
    return redirect('/devices/')


class ComingSoonView(TemplateView):
    template_name = 'common/coming-soon.html'


def page_404(request, *args, **kwargs):
    return render(request, 'common/page-404.html')


def page_500(request, *args, **kwargs):
    return render(request, 'common/page-500.html')

