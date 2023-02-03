from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.list import ListView

from .models import APIKey
from .forms import CreateAPIKeyForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView


class ApiKeysView(ListView):
    model = APIKey
    template_name = "api_control/api-keys.html"
    context_object_name = 'api_keys'
    paginate_by = 6

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        response = {}
        return JsonResponse(response)


class CreateApiKeyView(CreateView):
    template_name = "api_control/api-keys.html"
    model = APIKey
    form_class = CreateAPIKeyForm

    def form_valid(self, form):
        print(form)
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

