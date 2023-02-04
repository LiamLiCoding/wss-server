from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect
from django.contrib import auth
from django.views.generic import View
from django.views.generic import TemplateView
from django.db.models import ObjectDoesNotExist

from .forms import UserLoginForm, UserRegisterForm, ResetPasswordForm
from .models import Users
from apps.email_control.models import VerifyCode


def redirect_to_login(request):
    return HttpResponse('login')


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
            return redirect('/email_control/email_verify/' + email)

        return render(request, self.template_name, self.get_context_data(message))


class LogoutView(View):
    template_name = 'accounts/logout.html'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return render(request, self.template_name)


class ResetPasswordSuccessView(TemplateView):
    template_name = 'accounts/reset_password_success.html'


class ResetPasswordView(TemplateView):
    template_name = 'accounts/reset_password.html'
    model = VerifyCode
    form_class = ResetPasswordForm

    def get_context_data(self, *args, **kwargs):
        context = {'form': self.form_class}
        code = kwargs.get('code', None)
        if code:
            context["code"] = code
        if args:
            context.update(*args)
        return context

    def post(self, request, *args, **kwargs):
        code = kwargs.get('code')
        try:
            code_record = self.model.objects.get(code=code, code_type='reset_password')
        except ObjectDoesNotExist:
            return render(request, self.template_name, self.get_context_data({
                'message': "This reset link is invalid or has expired.",
                'code': code
            }))

        email = code_record.email
        reset_form = self.form_class(request.POST)
        if reset_form.is_valid():
            password = reset_form.cleaned_data.get('password')
            confirmed_password = reset_form.cleaned_data.get('confirmed_password')
            if password == confirmed_password:
                user = Users.objects.get(email=email)
                if isinstance(user, Users):
                    user.set_password(password)
                    user.save()
                    code_record.delete()
                    return redirect("/accounts/reset_password_success")
            else:
                return render(request, self.template_name, self.get_context_data({
                    'message': "The two entered passwords do not match",
                    'code': code
                }))
        return render(request, self.template_name, self.get_context_data({
            'message': "Invalid request. Please check you input.",
            'code': code
        }))






