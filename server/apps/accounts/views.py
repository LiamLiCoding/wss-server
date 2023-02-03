from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import auth
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist

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
