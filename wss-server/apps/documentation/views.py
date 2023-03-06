from apps.accounts.mixins import UserSettingsMixin
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class DocWsDataCommunicationView(LoginRequiredMixin, UserSettingsMixin, TemplateView):
    template_name = "documentation/websocket_access.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_info())
        if args:
            context.update(*args)
        return context
