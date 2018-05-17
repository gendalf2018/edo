# -*- coding: utf-8 -*-
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

from .forms import EdoUserCreationForm
from .models import EdoUser

def regLogin(request):
    rp = request.POST
    regform = EdoUserCreationForm()
    loginform = AuthenticationForm()
    if request.method == 'POST':
        if rp['formtype'] and rp['formtype'] == 'login':
            print("FORMTYPE", rp['formtype'], rp)
            loginform = AuthenticationForm(rp)
            user = authenticate(request, username=rp.get('username'), password=rp.get('password'))
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request,
                              'profile/registration.html',
                              {'regform': regform, 'loginform': loginform})

        elif rp['formtype'] and rp['formtype'] == 'registration':
            # print("FORMTYPE", rp['formtype'], rp)
            regform = EdoUserCreationForm(rp)
            if regform.is_valid():
                regform.save()
                user = authenticate(request, username=rp.get('email'), password=rp.get('password1'))
                if user is not None:
                    user.username = user.email
                    user.save()
                    login(request, user)
                    return HttpResponseRedirect('/')
    return render(request, 'profile/registration.html', {'regform': regform, 'loginform': loginform})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
