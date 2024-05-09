from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import CharField



class LoginForm(forms.Form):
    username = forms.CharField(max_length=5)
    password = forms.CharField(widget=forms.PasswordInput)