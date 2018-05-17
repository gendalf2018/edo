# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import (ReadOnlyPasswordHashField,
                                       UserCreationForm,
                                       AuthenticationForm)

from .models import EdoUser


class EdoUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение', widget=forms.PasswordInput)

    class Meta:
        model = EdoUser
        fields = ('email',
                  'first_name',
                  'last_name',
                #   'father_name',
                  'occupation',
                  'groups',
                  'phone',
                  'skype')

class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = EdoUser
        fields = ('email', 'password')

    def clean_password(self):
        return self.initial["password"]
