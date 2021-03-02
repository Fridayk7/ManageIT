"""
Copyright (c) 2019 - present AppSeed.us
"""
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from projects.models import Project, ProjectEmployeeRole
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

    print('LOGIN HERE')
    print('profile_id', profile_id)
    print('profile_id', project_id)
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

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def user_logout(request):
    logout(request)
    return redirect('accounts-login')


@login_required(login_url='accounts-login')
def user_account(request):

    return render(request, 'accounts/user_account.html')


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
    return render(request, "accounts/register.html", {})
