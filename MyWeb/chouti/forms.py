# -*- coding:utf-8 -*-
# @Time     : 2017-06-01 13:29
# @Author   : gck1d6o
# @Site     : 
# @File     : forms.py
# @Software : PyCharm

from django import forms
from django.forms import fields, widgets
from .models import UserInfo, News


class RegisterForm(forms.ModelForm):
    username = fields.CharField(
        required=True,
        min_length=4,
        max_length=32,
        error_messages={'required': '用户名不能为空'},
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    password = fields.CharField(
        required=True,
        min_length=6,
        max_length=32,
        error_messages={'required': '密码不能为空'},
        widget=widgets.PasswordInput(attrs={'class': 'form-control'})
    )
    email = fields.CharField(
        required=True,
        max_length=32,
        error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'},
        widget=widgets.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserInfo
        fields = ["username", "password", "email"]


class LoginForm(forms.Form):
    login_username = fields.CharField(
        required=True,
        error_messages={'required': '用户名不能为空'},
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    login_password = fields.CharField(
        required=True,
        error_messages={'required': '密码不能为空'},
        widget=widgets.PasswordInput(attrs={'class': 'form-control'})
    )


class ImageNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["image"]
