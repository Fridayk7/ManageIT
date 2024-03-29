# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "value": "TEST",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "value": "APS12_ZZS8",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First name",
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last name",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UserDataUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        exclude = ['user']


class ImageUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        exclude = ['user']
