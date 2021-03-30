from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from projects.models import ProjectEmployeeRole

@login_required(login_url='accounts-login')
def home(request):
    profile_id = request.session.get('ref_profile')
    project_id = request.session.get('ref_project')

    print('HOME HERE')
    print('profile_id', profile_id)
    print('profile_id', project_id)
    return render(request, 'pages/home.html')


@login_required(login_url='accounts-login')
def projects(request):
    return render(request, 'pages/projects.html')


@login_required(login_url='accounts-login')
def notifications(request):
    return render(request, 'pages/notifications.html')
