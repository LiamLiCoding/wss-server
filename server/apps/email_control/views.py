from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect


class TwoStepVerifyView(TemplateView):
    template_name = 'email_control/two_step_verify.html'

    def get(self, request, *args, **kwargs):
        request_email = kwargs.get('request_email', '')
        context = {
            'request_email': request_email,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return redirect('/accounts/login/')
