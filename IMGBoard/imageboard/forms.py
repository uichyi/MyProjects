from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from imageboard.models import *


class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', )

    def check_pass(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']

        if password != password_confirm:
            raise ValidationError("Passwords must be equal")

        return password


class CreatePost(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ('body', )


class CreateThread(forms.ModelForm):
    title = forms.CharField(max_length=50)

    class Meta:
        model = Thread
        fields = ('title', )
