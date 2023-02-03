import secrets
import datetime

from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import APIKey
from .forms import CreateAPIKeyForm, DeleteAPIKeyForm


class ApiKeysView(ListView):
    model = APIKey
    template_name = "api_control/api-keys.html"
    context_object_name = 'api_keys'
    paginate_by = 6
    create_form = CreateAPIKeyForm
    delete_form = DeleteAPIKeyForm

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = self.create_form()
        context['delete_form'] = self.delete_form()
        return context


class CreateApiKeyView(CreateView):
    template_name = "api_control/api-keys.html"
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


class DeleteApiKeyView(DeleteView):
    template_name = "api_control/api-keys.html"
    model = APIKey
    form_class = DeleteAPIKeyForm
    success_url = reverse_lazy('api-key')



