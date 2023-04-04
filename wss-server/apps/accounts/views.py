import requests
import datetime
from user_agents import parse
from django.contrib import auth
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from django.utils import timezone
from urllib.parse import urlencode
from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.db.models import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.shortcuts import HttpResponse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from . import send_email
from .mixins import UserSettingsMixin
from .models import Users, VerifyCode, UserSettings, LoginHistory
from .forms import UserLoginForm, UserRegisterForm, ResetPasswordForm


def get_device_info(request):
    device_info = {
        "is_mobile": request.user_agent.is_mobile,  # returns True
        "is_tablet": request.user_agent.is_tablet,  # returns False
        "is_touch_capable": request.user_agent.is_touch_capable,  # returns True
        "is_pc": request.user_agent.is_pc,  # returns False
        "is_bot": request.user_agent.is_bot,  # returns False
    
        # Accessing user agent's browser attributes
        "browser": request.user_agent.browser.family,  # returns 'Mobile Safari'
        "browser_version": request.user_agent.browser.version_string,  # returns '5.1'
    
        # Operating System properties
        "device_os": request.user_agent.os.family,  # returns 'iOS'
        "device_os_version": request.user_agent.os.version_string,  # returns '5.1'
    
        # Device properties
        "device": request.user_agent.device.family,  # returns 'iPhone'
    }

    return device_info


def save_login_history(user_obj, device_info):
    history = LoginHistory()
    history.user = user_obj
    history.device = device_info['device']
    history.device_os = device_info['device_os']
    history.device_os_version = device_info['device_os_version']
    history.browser = device_info['browser']
    history.browser_version = device_info['browser_version']
    history.is_pc = device_info['is_pc']
    history.is_mobile = device_info['is_mobile']
    history.location = None

    history.save()


def redirect_to_login(request):
    return HttpResponse('login')


class LoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    @staticmethod
    def get_oauth_url(url, client_id, redirect_uri='', scope='', response_type=''):
        parameter = {'client_id': client_id}
        if redirect_uri:
            parameter.update({'redirect_uri': redirect_uri})
        if scope:
            parameter.update({'scope': scope})
        if scope:
            parameter.update({'response_type': response_type})
        data = urlencode(parameter)
        return url + "?" + data

    def get_context_data(self, *args):
        context = {'login_form': self.form_class,
                   'github_oauth_url': self.get_oauth_url('https://github.com/login/oauth/authorize',
                                                          settings.GITHUB_CLIENT_ID),
                   'google_oauth_url': self.get_oauth_url('https://accounts.google.com/o/oauth2/auth',
                                                          client_id=settings.GOOGLE_CLIENT_ID,
                                                          redirect_uri='https://wssweb.net/accounts/oauth/google/',
                                                          scope='https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
                                                          response_type='code')}
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
                    save_login_history(self.request.user, get_device_info(request))
                    return redirect(self.get_success_url())
                else:
                    verify_tips = "Your account have not been verified."
                    return render(request, self.template_name,
                                  self.get_context_data({"verify_tips": verify_tips, "verify_email": user.email}))

        return render(request, self.template_name, self.get_context_data({"message": message}))


class OauthBaseView(View):
    access_token_url = None
    user_api = None
    client_id = None
    client_secret = None

    def authenticate(self, *args, **kwargs):
        """
        A function to authenticate user, needs to be rewritten
        """
        pass

    def get(self, request, *args, **kwargs):
        access_token = self.get_access_token(request)
        user_info = self.get_user_info(access_token)
        return self.authenticate(user_info)

    def get_access_token(self, request):
        headers = {'Accept': 'application/json'}
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': request.GET['code']
        }
        results = requests.post(self.access_token_url, data, headers=headers, timeout=1)
        results = results.json()

        if 'access_token' in results:
            return results['access_token']
        else:
            raise PermissionDenied

    def get_user_info(self, access_token):
        data = {
            'access_token': access_token,
        }
        results = requests.get(self.user_api, data, timeout=1)
        user_info = results.json()
        return user_info

    def get_success_url(self):
        if 'next' in self.request.session:
            return self.request.session.pop('next')
        else:
            return '/'


class GitHubOAuthView(OauthBaseView):
    access_token_url = 'https://github.com/login/oauth/access_token'
    user_api = 'https://api.github.com/user'
    client_id = settings.GITHUB_CLIENT_ID
    client_secret = settings.GITHUB_CLIENT_SECRET

    def authenticate(self, user_info):
        """
        github use info return keys:
        ['login', 'id', 'node_id', 'avatar_url', 'gravatar_id', 'url', 'html_url', 'followers_url',
        'following_url', 'gists_url', 'starred_url', 'subscriptions_url', 'organizations_url',
        'repos_url', 'events_url', 'received_events_url', 'type', 'site_admin', 'name', 'company',
        'blog', 'location', 'email', 'hireable', 'bio', 'twitter_username', 'public_repos', 'public_gists',
        'followers', 'following', 'created_at', 'updated_at']
        """

        user = Users.objects.filter(oauth_id=user_info['id'])
        if not user:
            user = Users.objects.create_user(username=user_info['login'],
                                             oauth_id=user_info['id'],
                                             email=user_info['email'],
                                             password='********',
                                             avatar=user_info['avatar_url'],
                                             )
            user_settings = UserSettings(user=user)
            user_settings.save()
        else:
            user = user[0]
        auth.login(self.request, user)
        save_login_history(self.request.user, get_device_info(self.request))
        self.request.session['user_name'] = user.username
        return redirect(self.get_success_url())


class GoogleOAuthView(OauthBaseView):
    access_token_url = 'https://oauth2.googleapis.com/token'
    user_api = 'https://www.googleapis.com/oauth2/v3/userinfo'
    client_id = settings.GOOGLE_CLIENT_ID
    client_secret = settings.GOOGLE_CLIENT_SECRET

    def get_access_token(self, request):
        headers = {'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': request.GET['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': 'https://wssweb.net/accounts/oauth/google/',
        }
        results = requests.post(self.access_token_url, data, headers=headers, timeout=1)
        results = results.json()

        if 'access_token' in results:
            return results['access_token']
        else:
            raise PermissionDenied

    def authenticate(self, user_info):
        """
        Google user info return keys:
        {'sub', 'name', 'given_name', 'family_name', 'picture', 'email', 'email_verified', 'locale', 'hd',}
        """
        user = Users.objects.filter(oauth_id=user_info['sub'])
        if not user:
            user = Users.objects.create_user(username=user_info['name'],
                                             oauth_id=user_info['sub'],
                                             email=user_info['email'],
                                             first_name=user_info['given_name'],
                                             last_name=user_info['family_name'],
                                             password='********',
                                             avatar=user_info['picture'],
                                             )
            user_settings = UserSettings(user=user)
            user_settings.save()
        else:
            user = user[0]
        auth.login(self.request, user)
        save_login_history(self.request.user, get_device_info(self.request))
        self.request.session['user_name'] = user.username
        return redirect(self.get_success_url())


class RegisterView(View):
    model = Users
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def get_context_data(self, message=None, *args):
        context = {'register_form': self.form_class,
                   'github_oauth_url': LoginView.get_oauth_url('https://github.com/login/oauth/authorize',
                                                          settings.GITHUB_CLIENT_ID),
                   'google_oauth_url': LoginView.get_oauth_url('https://accounts.google.com/o/oauth2/auth',
                                                          client_id=settings.GOOGLE_CLIENT_ID,
                                                          redirect_uri='https://wssweb.net/accounts/oauth/google/',
                                                          scope='https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
                                                          response_type='code')}
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

            user = self.model.objects.create_user(username=username, password=password, email=email)
            user_settings = UserSettings(user=user)
            user_settings.save()
            return redirect('/accounts/email_verify/' + email)

        return render(request, self.template_name, self.get_context_data(message))


class LogoutView(View):
    template_name = 'accounts/logout.html'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return render(request, self.template_name)


class AccountSettings(LoginRequiredMixin, UserSettingsMixin, TemplateView):
    template_name = 'accounts/account-settings.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_info())
        profile_complete_percent = round((bool(self.request.user.first_name) + bool(self.request.user.last_name) +
                                        bool(self.request.user.phone))/3, 4)*100
        context.update({"profile_complete_percent": profile_complete_percent})
        try:
            user_settings = UserSettings.objects.get(user=self.request.user)
            if user_settings:
                context['detection_Email_notification'] = user_settings.detection_Email_notification
                context['detection_SMS_notification'] = user_settings.detection_SMS_notification
                context['update_notification'] = user_settings.update_notification
                context['web_notification'] = user_settings.web_notification
        except ObjectDoesNotExist:
            user_settings = UserSettings(user=self.request.user)
            user_settings.save()
        if args:
            context.update(*args)
        return context


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


class EmailVerify(TemplateView):
    template_name = 'accounts/two_step_verify.html'
    model = VerifyCode

    def __init__(self, *args, **kwargs):
        super(EmailVerify, self).__init__(*args, **kwargs)
        self.request_email = ''

    def get_context_data(self, *args):
        context = {}
        if args:
            context.update(*args)
        return context

    def get(self, request, *args, **kwargs):
        self.request_email = kwargs.get('request_email', '')
        # Determine whether the request is invalid
        try:
            user = Users.objects.get(email=self.request_email)
        except ObjectDoesNotExist:
            return render(request, self.template_name, self.get_context_data({
                'request_email': self.request_email,
                'message': 'Invalid request, the user does not exist in our database',
            }))

        if user.is_verified:
            return render(request, self.template_name, self.get_context_data({
                'request_email': self.request_email,
                'message': 'The user has already verified the email address and does not need to re-authenticate.',
            }))

        try:
            self.model.objects.get(email=self.request_email, code_type='verify_email')
            message = 'You have already request for verification code, ' \
                      'please check your email or click resend button.'
            return render(request, self.template_name, self.get_context_data({
                'request_email': self.request_email,
                'message': message,
            }))
        except ObjectDoesNotExist:
            send_email.send_digit_code_email(self.request_email, 'verify_email')

        return render(request, self.template_name, self.get_context_data({
            'request_email': self.request_email,
        }))

    def verify_email(self, code):
        try:
            code_record = self.model.objects.get(code=code, code_type='verify_email')
            if code_record.expiration_time > timezone.now():
                try:
                    user = Users.objects.get(email=self.request_email)
                    user.is_verified = True
                    user.save()
                    code_record.delete()
                    return True
                except ObjectDoesNotExist:
                    return False
        except ObjectDoesNotExist:
            return False
        return False

    def post(self, request, *args, **kwargs):
        self.request_email = kwargs.get('request_email', '')
        digit1 = request.POST.get('digit1')
        digit2 = request.POST.get('digit2')
        digit3 = request.POST.get('digit3')
        digit4 = request.POST.get('digit4')
        input_code = digit1 + digit2 + digit3 + digit4
        if self.verify_email(input_code):
            return redirect('/accounts/login/')
        else:
            message = 'Your verification code is not correct. Please try again.'
            return render(request, self.template_name,
                          self.get_context_data({'message': message, 'request_email': self.request_email}))


class ResendEmailVerify(EmailVerify):
    template_name = 'accounts/two_step_verify.html'
    model = VerifyCode

    def get(self, request, *args, **kwargs):
        self.request_email = kwargs.get('request_email', '')
        try:
            code_record = self.model.objects.get(email=self.request_email, code_type='verify_email')
            if code_record.send_time >= timezone.now() - datetime.timedelta(minutes=1):
                return render(request, self.template_name, self.get_context_data({
                    'request_email': self.request_email,
                    'message': 'Your request is too frequent, please try again {:.0f}s later'.format(
                        (code_record.send_time - (timezone.now() - datetime.timedelta(minutes=1))).total_seconds()
                    ),
                }))
            else:
                code_record.delete()
        except ObjectDoesNotExist:
            return render(request, self.template_name, self.get_context_data({
                'request_email': self.request_email,
                'message': 'Invalid resend request',
            }))

        # Verify user validation
        try:
            user = Users.objects.get(email=self.request_email)
            if user.is_verified:
                return render(request, self.template_name, self.get_context_data({
                    'request_email': self.request_email,
                    'message': 'The user has already verified the email address and does not need to re-authenticate.',
                }))
        except ObjectDoesNotExist:
            return render(request, self.template_name, self.get_context_data({
                'request_email': self.request_email,
                'message': 'Invalid request, the user does not exist in our database',
            }))

        try:
            self.model.objects.get(email=self.request_email, code_type='verify_email')
            message = 'You have already requested for a verification code, ' \
                      'please check your email or click resend button.'
            return render(request, self.template_name, self.get_context_data({
                'request_email': self.request_email,
                'message': message}))
        except ObjectDoesNotExist:
            send_email.send_digit_code_email(self.request_email, 'verify_email')

        return render(request, self.template_name, self.get_context_data({
            'request_email': self.request_email,
            'resend_message': 'The verification code has been resent to your email'}))


class EmailVerifySuccessView(TemplateView):
    template_name = 'accounts/email_verify_success.html'


class ForgetPasswordView(TemplateView):
    template_name = 'accounts/forget_password.html'
    model = VerifyCode

    def get_context_data(self, *args):
        context = {}
        if args:
            context.update(*args)
        return context

    def get(self, request, *args, **kwargs):
        message = ''
        return render(request, self.template_name,
                      self.get_context_data({'message': message}))

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        try:
            code_record = self.model.objects.get(email=email, code_type='reset_password')
            if code_record.send_time >= timezone.now() - datetime.timedelta(minutes=1):
                return render(request, self.template_name, self.get_context_data({
                    'message': 'Your request is too frequent, please try again {:.0f}s later'.format(
                        (code_record.send_time - (timezone.now() - datetime.timedelta(minutes=1))).total_seconds()
                    ),
                }))
            else:
                code_record.delete()
        except ObjectDoesNotExist:
            pass

        try:
            Users.objects.get(email=email)
            send_email.send_reset_password_link_email(email, 'reset_password')
            return redirect(reverse('reset_link_sent'))
        except ObjectDoesNotExist:
            return render(request, self.template_name, self.get_context_data({
                'message': 'Account does not exist!',
            }))


class ResetLinkSentView(TemplateView):
    template_name = 'accounts/reset_link_sent.html'


class ChangePersonalInfoAPI(LoginRequiredMixin, APIView):
    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        username = request.POST.get('username')

        self.request.user.first_name = first_name
        self.request.user.last_name = last_name
        self.request.user.phone = phone
        if username:
            self.request.user.username = username
        self.request.user.save()
        return Response(status=status.HTTP_200_OK)


class ChangePasswordAPI(LoginRequiredMixin, APIView):
    def post(self, request):
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if old_password:
            user = auth.authenticate(email=self.request.user.email, password=old_password)
            if isinstance(user, Users) and new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class NotificationSettingsAPI(LoginRequiredMixin, APIView):
    def post(self, request):
        notification_type = request.POST.get('notification_type')
        value = request.POST.get('value')
        value = False if value == 'false' else True
        data = {notification_type: value}

        user_settings = UserSettings.objects.filter(user=self.request.user)
        if user_settings:
            user_settings.update(**data)

        return Response(status=status.HTTP_200_OK)


class DeleteAccountAPI(LoginRequiredMixin, APIView):
    def post(self, request):
        confirm_password = request.POST.get('confirm_password')
        if confirm_password:
            user = auth.authenticate(email=self.request.user.email, password=confirm_password)
            if isinstance(user, Users):
                auth.logout(request)
                user.delete()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
