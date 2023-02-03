from django.forms import ModelForm, HiddenInput, TextInput
from .models import APIKey


class CreateAPIKeyForm(ModelForm):
    class Meta:
        model = APIKey
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'id': "api-key-name",
                                     "placeholder": "Enter api key name"}),
        }
