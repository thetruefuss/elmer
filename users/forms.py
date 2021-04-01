#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

from .models import Profile


class SignupForm(forms.ModelForm):
    """
    Form that handles signup data.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserEditForm(forms.ModelForm):
    """
    Form that handles user data.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    """
    Form that handles profile data.
    """
    class Meta:
        model = Profile
        fields = ('dob', 'dp')
