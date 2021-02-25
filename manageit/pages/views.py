from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='accounts-login')
def home(request):
    return render(request, 'pages/home.html')


@login_required(login_url='accounts-login')
def projects(request):
    return render(request, 'pages/projects.html')


@login_required(login_url='accounts-login')
def account(request):
    return render(request, 'pages/account.html')


@login_required(login_url='accounts-login')
def notifications(request):
    return render(request, 'pages/notifications.html')
