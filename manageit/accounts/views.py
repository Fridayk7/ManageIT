"""
Copyright (c) 2019 - present AppSeed.us
"""
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm
from .decorators import unauthenticated_user


@unauthenticated_user
def register(request):

    msg = None
    success = False
    profile_id = request.session.get('ref_profile')
    print('profile_id', profile_id)

    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            if profile_id is not None:
                recommended_by_profile = Profile.objects.get(id=profile_id)

                instance = form.save()
                registered_user = User.objects.get(id=instance.id)
                registered_profile = Profile.objects.get(user=registered_user)
                registered_profile.recommended_by = recommended_by_profile.user
                registered_profile.save()
            else:
                form.save()

            msg = 'User created'
            success = True
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, 'accounts/register.html', {'form': form, 'msg': msg, 'success': success})

    # msg = None
    # success = False
    #
    # if request.method == 'POST':
    #     form = SignUpForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password1')
    #         user = authenticate(username=username, password=password)
    #         # Profile.objects.create(
    #         #     user=user,
    #         # )
    #
    #         msg = 'User created'
    #         success = True
    #
    #     else:
    #         msg = 'Form is not valid'
    # else:
    #     form = SignUpForm()
    #
    # return render(request, 'accounts/register.html', {'form': form, 'msg': msg, 'success': success})


@unauthenticated_user
def user_login(request):

    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts-account')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def user_logout(request):
    logout(request)
    return redirect('accounts-login')


@login_required(login_url='accounts-login')
def user_account(request):

    return render(request, 'accounts/user_account.html')


def get_code(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profile = Profile.objects.get(code=code)
        request.session['ref_profile'] = profile.id
        print('id', profile.id)
    except:
        pass
    print(request.session.get_expiry_date())
    return render(request, "accounts/register.html", {})
