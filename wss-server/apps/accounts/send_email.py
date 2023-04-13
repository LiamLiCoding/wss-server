import datetime
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from apps.utils.verification_code import generate_digit_verification_code, generate_str_verification_code

from apps.accounts.models import VerifyCode, UserSettings


def send_digit_code_email(email, code_type="verify_email"):
    send_record = VerifyCode() 
    code = generate_digit_verification_code(4)
    send_record.code = code
    send_record.email = email
    send_record.code_type = code_type
    send_record.expiration_time = timezone.now() + datetime.timedelta(minutes=10)
    send_record.save()

    email_title = "[WSS] Please verify your email"
    email_body = """
Hey!

Thanks for creating an account on WSS!

Enter your 4-digit verification code to verify your Email. 

Verification code: {}
The verification code is valid within ten minutes.

If you have difficulty on login or registration of WSS, feel free to contract me: wss-web@outlook.com

Thanks,
From WSS developer.
""".format(code)
    send_status = send_mail(email_title, email_body, settings.DEFAULT_FROM_EMAIL, [email])
    print("email sent", send_status)
    if not send_status:
        return False


def send_reset_password_link_email(email, code_type="reset_password"):
    send_record = VerifyCode()
    code = generate_str_verification_code(32)
    send_record.code = code
    send_record.email = email
    send_record.code_type = code_type
    send_record.expiration_time = timezone.now() + datetime.timedelta(minutes=10)
    send_record.save()

    reset_link = "https://wssweb.net/accounts/reset_password/{}".format(code)
    email_title = "[WSS] Reset your password"
    text_content = '''
We just received a password request for your account. To choose a new password, please click the link below. This link will be expire in 3 hours.

{}

If you didn't request this change, please ignore this message.

Thank you,
WSS developer.
    '''.format(reset_link)

    html_content = """
<table class="body-wrap" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; width: 100%; background-color: transparent; margin: 0;">
    <tr style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
        <td style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0;" valign="top"></td>
        <td class="container" width="600" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; display: block !important; max-width: 600px !important; clear: both !important; margin: 0 auto;" valign="top">
            <div class="content" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; max-width: 600px; display: block; margin: 0 auto; padding: 20px;">
                <table class="main" width="100%" cellpadding="0" cellspacing="0" itemprop="action" itemscope itemtype="http://schema.org/ConfirmAction" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; border-radius: 3px; margin: 0; border: none;">
                    <tr style="font-family: 'Roboto', sans-serif; font-size: 14px; margin: 0;">
                        <td class="content-wrap" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; color: #495057; font-size: 14px; vertical-align: top; margin: 0;padding: 30px; box-shadow: 0 3px 15px rgba(30,32,37,.06); ;border-radius: 7px; background-color: #fff;" valign="top">
                            <meta itemprop="name" content="Confirm Email" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;" />
                            <table width="100%" cellpadding="0" cellspacing="0" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                <tr style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                    <td class="content-block" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                        <div style="text-align: center;">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-lock" style="color: #3bad71;fill: rgba(10,179,156,.16); height: 30px; width: 30px;"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                                        </div>
                                    </td>
                                </tr>
                                <tr style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                    <td class="content-block" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 24px; vertical-align: top; margin: 0; padding: 0 0 10px;  text-align: center;" valign="top">
                                        <h5 style="font-family: 'Roboto', sans-serif; margin-bottom: 0px;font-weight: 500; line-height: 1.5;">Change or reset your password</h5>
                                    </td>
                                </tr>
                                <tr style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                    <td class="content-block" style="font-family: 'Roboto', sans-serif; color: #878a99; box-sizing: border-box; font-size: 15px; vertical-align: top; margin: 0; padding: 0 0 12px; text-align: center;" valign="top">
                                        <p style="margin-bottom: 13px; line-height: 1.5;">We just received a password request for your account. To choose a new password, please click the button below. This link will be expire in 3 hours</p>
                                    </td>
                                </tr>
                                <tr style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                    <td class="content-block" itemprop="handler" itemscope itemtype="http://schema.org/HttpActionHandler" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 22px; text-align: center;" valign="top">
                                        <a href="{}" itemprop="url" style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: .8125rem; color: #FFF; text-decoration: none; font-weight: 400; text-align: center; cursor: pointer; display: inline-block; border-radius: .25rem; text-transform: capitalize; background-color: #4b38b3; margin: 0; border-color: #4b38b3; border-style: solid; border-width: 1px; padding: .5rem .9rem;box-shadow: 0 3px 3px rgba(56,65,74,0.1);">Reset Password</a>
                                    </td>
                                </tr>
                                <tr style="font-family: 'Roboto', sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                    <td class="content-block" style="font-family: 'Roboto', sans-serif; color: #878a99; box-sizing: border-box; font-size: 15px; vertical-align: top; margin: 0; padding: 0 0 12px; text-align: center;" valign="top">
                                        <p style="margin-bottom: 13px; line-height: 1.5;">If you didn't request this change, please ignore this message.</p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
                <div style="text-align: center; margin: 28px auto 0px auto;">
                    <h4>Need Help ?</h4>
                    <p style="color: #878a99;">Please send and feedback or bug info to <a href="" style="font-weight: 500px;">wss-web@outlook.com</a></p>
                    <p style="font-family: 'Roboto', sans-serif; font-size: 14px;color: #98a6ad; margin: 0px;">2023 @WSS</p>
                </div>
            </div>
        </td>
    </tr>
</table>
<!-- end table -->
    """.format(reset_link)
    msg = EmailMultiAlternatives(email_title, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_detection_warning_email(user_id, email, detection_event_type, resource_url):
    # Check availability
    availability = False
    try:
        user_settings = UserSettings.objects.get(id=user_id)
        if user_settings:
            availability = user_settings.detection_Email_notification
    except ObjectDoesNotExist:
        availability = False

    if not availability:
        return
    email_title = "[WSS] Intruder Detection Event"

    text_content = """
    Hey!

    This is a intruder detection event from WSS!

    WSS has detect an intruder at time {}, raise **EVENT{}**

    Intruder detection resource url: {}

    Thanks,
    From WSS developer.
    """.format(timezone.now(), detection_event_type, resource_url)
    html_content = """
<p>Hey!</p>
<p>This is an intruder detection event from WSS!</p>
<p>WSS has detected an intruder at time <b>{}</b>. Raised <b>EVENT{}</b></p>
<p>System will enter <b>Mode{}</b></p>
<p>Intruder detection resource url: <a href="http://{}" target="_blank"><b>Click here to view Detection image or video</b></a></p>
<p>Thanks,</p>
<p>From WSS developer.</p>
    """.format(timezone.now(), detection_event_type, detection_event_type, resource_url)
    msg = EmailMultiAlternatives(email_title, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
