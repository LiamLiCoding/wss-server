
from django.views.generic.list import ListView

from .models import APIKey


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
