"""
Copyright (c) 2019 - present AppSeed.us
"""
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from projects.models import Project, ProjectEmployeeRole
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from datetime import datetime
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm, UserDataUpdateForm, ImageUpdateForm
from .decorators import unauthenticated_user
from projects.models import Task


@unauthenticated_user
def register(request):

    msg = None
    success = False
    profile_id = request.session.get('ref_profile')
    project_id = request.session.get('ref_project')

    print("Register")
    print('profile_id', profile_id)
    print('profile_id', project_id)

    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            if profile_id is not None and project_id is not None:
                recommended_by_profile = Profile.objects.get(id=profile_id)

                instance = form.save()
                registered_user = User.objects.get(id=instance.id)
                registered_profile = Profile.objects.get(user=registered_user)
                registered_profile.recommended_by = recommended_by_profile.user
                registered_profile.save()

                project = Project.objects.get(id=project_id)
                project_staff = ProjectEmployeeRole(project=project, user=registered_profile, user_role=ProjectEmployeeRole.STAFF)
                project_staff.save()
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
    profile_id = request.session.get('ref_profile')
    project_id = request.session.get('ref_project')

    # print('LOGIN HERE')
    # print('profile_id', profile_id)
    # print('profile_id', project_id)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                if profile_id is not None and project_id is not None:
                    profile = Profile.objects.get(user__id=user.id)
                    project_employee_check = None
                    try:
                        project_employee_check = ProjectEmployeeRole.objects.filter(project_id=project_id).get(user__id=profile.id)
                    except ProjectEmployeeRole.DoesNotExist:
                        project_employee_check = None

                    if project_employee_check is None:
                        project = Project.objects.get(id=project_id)
                        project_employee = ProjectEmployeeRole(user=profile, project=project, user_role=ProjectEmployeeRole.STAFF)
                        project_employee.save()
                login(request, user)
                return redirect('accounts-account')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {'form': form, 'msg': msg})


def user_logout(request):
    logout(request)
    return redirect('accounts-login')

# https://www.youtube.com/watch?v=aNk2CAkHvlE
@login_required(login_url='accounts-login')
def user_account(request):
    current_user = request.user
    current_user_profile_image = request.user.profile

    form = UserDataUpdateForm(instance=current_user)
    form2 = ImageUpdateForm(instance=current_user_profile_image)

    user_profile = Profile.objects.get(user=current_user)
    tasks = Task.objects.filter(user=user_profile).filter(active=True)

    if request.method == 'POST':
        form = UserDataUpdateForm(request.POST, instance=current_user)
        form2 = ImageUpdateForm(request.POST, request.FILES, instance=current_user_profile_image)
        if form2.is_valid():
            form2.save()
        if form.is_valid():
            form.save()

    context = {'form': form, 'form2': form2, 'tasks': tasks}

    # if request.method == 'POST':
    #     u_form = UserUpdateForm()
    #     p_form = ProfileUpdateForm()
    # else:
    #     u_form = UserUpdateForm()
    #
    # context = {
    #     'u_form': u_form,
    #     'p_form': p_form,
    # }

    return render(request, 'accounts/user_account.html', context)


def get_code(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    project_code = str(kwargs.get('project_code'))
    try:
        profile = Profile.objects.get(code=code)
        request.session['ref_profile'] = profile.id
        project = Project.objects.get(code=project_code)
        request.session['ref_project'] = project.id

        print('id', profile.id)
        print('id', project.id)
    except:
        pass
    print(request.session.get_expiry_date())
    return render(request, 'accounts/register.html', {})


# @login_required(login_url='accounts-login')
# def goPremium(request):
#     return render()

@login_required(login_url='accounts-login')
def upgrade_to_premium(request):
    return render(request, 'accounts/payment.html')


@login_required(login_url='accounts-login')
def payment_complete(request):
    current_user = request.user
    premium = "Premium"
    user_profile = Profile.objects.get(user=current_user)
    current_subscription_user = Subscription.objects.get(user=user_profile)
    type_premium = SubscriptionType.objects.get(name=premium)
    # current_subscription_user == type_premium
    # 2 subscription.current_user = subscription_type
    # upgrade = Subscription(subscription_type=type_premium, user=user_profile, date_changed=datetime.now())
    current_subscription_user.subscription_type = type_premium
    current_subscription_user.date_changed = datetime.now()
    current_subscription_user.save()
    print(current_subscription_user.subscription_type)

    template = render_to_string('accounts/payment_email_template.html',
                                {'receiver_name': current_user.first_name})

    email = EmailMessage(
        'Your payment was successful!',
        template,
        settings.EMAIL_HOST_USER,
        [current_user.email],
    )

    email.fail_silently = False
    email.send()

    body = json.loads(request.body)
    print('BODY', body)
    return JsonResponse('Payment completed!', safe=False)
