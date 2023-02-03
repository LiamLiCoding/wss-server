from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import auth
from django.views.generic import View

from .forms import UserLoginForm, UserRegisterForm
from .models import Users


def redirect_to_login(request):
    return redirect('/accounts/login/')


class LoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get_context_data(self, *args):
        context = {'login_form': self.form_class}
        if args:
            context.update(*args)
        return context

    def get_success_url(self):
        if 'next' in self.request.session:
            return self.request.session.pop('next')
        else:
            return '/'

    def get(self, request, *args, **kwargs):
        if 'next' in self.request.GET:
            self.request.session['next'] = self.request.GET['next']

        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        login_form = self.form_class(request.POST)
        message = "Your email and password didn't match any record of our databases. Please try again"

        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            remember_status = request.POST.get('remember_checkbox')  # None or 'on'
            user = auth.authenticate(username=username, password=password)
            if isinstance(user, Users):
                if remember_status:
                    pass
                request.session['user_name'] = user.username
                auth.login(self.request, user)
                return redirect(self.get_success_url())

        return render(request, self.template_name, self.get_context_data({"message": message}))


class RegisterView(View):
    model = Users
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def get_context_data(self, *args):
        context = {'register_form': self.form_class}
        if args:
            context.update(*args)
        return context

    def get_success_url(self):
        if 'next' in self.request.session:
            return self.request.session.pop('next')
        else:
            return '/'

    def get(self, request, *args, **kwargs):
        if 'next' in self.request.GET:
            self.request.session['next'] = self.request.GET['next']

        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        register_form = self.form_class(request.POST)
        message = ""

        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password')
            email = register_form.cleaned_data.get('email')
            same_email = self.model.objects.filter(email=email)
            if same_email:
                message = "The email is taken. Try another."
                return render(request, 'accounts/register.html', {"message": message})

            user = self.model.objects.create_user(username=username, password=password, email=email)
            return redirect('/accounts/login/')

        return render(request, self.template_name, self.get_context_data({"message": message}))


class LogoutView(View):
    template_name = 'accounts/logout.html'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return render(request, self.template_name)
