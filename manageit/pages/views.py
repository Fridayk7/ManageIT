from django.shortcuts import render

def home(request):
    return render(request, 'pages/home.html')

def projects(request):
    return render(request, 'pages/projects.html')

def account(request):
    return render(request, 'pages/account.html')

def notifications(request):
    return render(request, 'pages/notifications.html')

