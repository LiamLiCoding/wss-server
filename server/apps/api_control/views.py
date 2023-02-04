import secrets
import datetime
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from apps.accounts.mixins import GetLoginInfoMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import APIKey
from .forms import CreateAPIKeyForm


class ApiKeysView(LoginRequiredMixin, GetLoginInfoMixin, ListView):
    model = APIKey
    template_name = "api_control/api-keys.html"
    context_object_name = 'api_keys'
    paginate_by = 6
    create_form = CreateAPIKeyForm

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_info())
        context['create_form'] = self.create_form()
        return context


class CreateApiKeyView(LoginRequiredMixin, CreateView):
    model = APIKey
    form_class = CreateAPIKeyForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.key = secrets.token_urlsafe(32)
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('api-key')


class DeleteApiKeyView(LoginRequiredMixin, DeleteView):
    model = APIKey
    success_url = reverse_lazy('api-key')



