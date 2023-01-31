from django import forms


class UserLoginForm(forms.Form):
    email = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                              'placeholder': "Your Email"}))
    password = forms.CharField(max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                 'placeholder': "password"}))

