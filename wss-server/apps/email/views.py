import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.db.models import ObjectDoesNotExist

from . import send_email
from .models import VerifyCode
from apps.accounts.models import Users


class EmailVerify(TemplateView):
    template_name = 'email_control/two_step_verify.html'
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
    template_name = 'email_control/two_step_verify.html'
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
            send_email.send_digit_code_email(self.request_email, 'register')

        return render(request, self.template_name, self.get_context_data({
            'request_email': self.request_email,
            'resend_message': 'The verification code has been resent to your email'}))


class EmailVerifySuccessView(TemplateView):
    template_name = 'email_control/email_verify_success.html'


class ForgetPasswordView(TemplateView):
    template_name = 'email_control/forget_password.html'
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
            return redirect('/email/reset_link_sent/')
        except ObjectDoesNotExist:
            return render(request, self.template_name, self.get_context_data({
                'message': 'Account does not exist!',
            }))


class ResetLinkSentView(TemplateView):
    template_name = 'email_control/reset_link_sent.html'

