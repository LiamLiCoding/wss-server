from django import forms


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=256, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', "id": "username",
                                                             'placeholder': "Your Username or Email"}))
    password = forms.CharField(max_length=256, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control pe-5 password-input',
                                                                 'placeholder': "Enter password", "id": "password-input"
                                                                 }))


class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=256, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control form-control-lg',
                                                             'placeholder': "Your Username or Email"}))
    password = forms.CharField(max_length=256, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg',
                                                                 'placeholder': "password"}))

