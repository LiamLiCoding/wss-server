from django import forms


class UserLoginForm(forms.Form):
    email = forms.CharField(max_length=256, required=True,
                               widget=forms.EmailInput(attrs={'class': 'form-control',  "id": "useremail",
                                                             'placeholder': "Enter email address"}))
    password = forms.CharField(max_length=256, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control pe-5 password-input',
                                                                 'placeholder': "Enter password", "id": "password-input"
                                                                 }))


class UserRegisterForm(forms.Form):
    email = forms.CharField(max_length=256, required=True,
                               widget=forms.EmailInput(attrs={'class': 'form-control',  "id": "useremail",
                                                             'placeholder': "Enter email address"}))
    username = forms.CharField(max_length=256, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control',  "id": "username",
                                                             'placeholder': "Enter username"}))
    password = forms.CharField(max_length=256, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control pe-5 password-input',
                                                                 "onpaste": "return false",
                                                                 "id": "password-input",
                                                                 "aria - describedby": "passwordInput",
                                                                 "pattern": "(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",
                                                                 'placeholder': "password"}))


class ForgetPasswordForm(forms.Form):
    email = forms.CharField(max_length=256, required=True,
                            widget=forms.EmailInput(attrs={'class': 'form-control', "id": "email",
                                                           'placeholder': "Enter email"}))

