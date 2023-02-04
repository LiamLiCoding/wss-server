#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/2/3 18:01
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu


from django.core.mail import send_mail
from django.conf import settings
from .gen_verifi_code import generate_digit_verification_code

from .models import ConfirmCode


def send_digit_code_email(email, send_type="register"):

    code = generate_digit_verification_code(4)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.send_time = datetime.datetime.now()
    email_record.save()
    # 初始化为空
    email_title = ""
    email_body = ""
    # 如果为注册类型
    if send_type == "register":
        email_title = "注册激活"
        # email_body = "请点击下面的链接激活你的账号:http://127.0.0.1:8000/active/{0}".format(code)
        email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if not send_status:
            return False

    if send_type == "retrieve":
        email_title = "找回密码"
        email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if not send_status:
            return False
    return True
