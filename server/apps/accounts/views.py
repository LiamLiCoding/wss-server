from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import auth
from django.views.generic import View
from django.views.generic import TemplateView

from .forms import UserLoginForm, UserRegisterForm, ForgetPasswordForm
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
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            remember_status = request.POST.get('remember_checkbox')  # None or 'on'
            user = auth.authenticate(email=email, password=password)
            if isinstance(user, Users):
                if remember_status:
                    pass
                if user.is_verified:
                    request.session['user_name'] = user.username
                    auth.login(self.request, user)
                    return redirect(self.get_success_url())
                else:
                    verify_tips = "Your account have not been verified."
                    return render(request, self.template_name,
                                  self.get_context_data({"verify_tips": verify_tips, "verify_email": user.email}))

        return render(request, self.template_name, self.get_context_data({"message": message}))


class RegisterView(View):
    model = Users
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def get_context_data(self, message=None, *args):
        context = {'register_form': self.form_class}
        if message:
            context['message'] = message
        if args:
            context.update(*args)
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/accounts/login/')
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
                message = "The email has been taken. Try another."
                return render(request, 'accounts/register.html', self.get_context_data(message))

            self.model.objects.create_user(username=username, password=password, email=email)
            return redirect('/email_control/email_verify/')

        return render(request, self.template_name, self.get_context_data(message))


class LogoutView(View):
    template_name = 'accounts/logout.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('/accounts/login/')
        return render(request, self.template_name)


class RegisterSuccessView(TemplateView):
    template_name = 'accounts/register_success.html'


class ForgetPasswordView(TemplateView):
    form_class = ForgetPasswordForm
    template_name = 'accounts/forget_password.html'

    def get_context_data(self, request_email, *args):
        print(request_email)
        return {}

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            print(email)
            return redirect('/accounts/login/')
        return render(request, self.template_name, self.get_context_data())


