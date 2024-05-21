from django import forms
from django.core.exceptions import ValidationError

from app.models import *


class LoginForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)