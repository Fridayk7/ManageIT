from django.shortcuts import render


def home(request):
    return render(request, 'pages/home.html')

def projects(request):
    return render(request, 'pages/projects.html')

def account(request):
    return render(request, 'pages/account.html')

def activity(request):
    return render(request, 'pages/activity.html')

def notifications(request):
    return render(request, 'pages/notifications.html')

def list(request):
    return render(request, 'pages/list.html')

def kanban(request):
    return render(request, 'pages/kanban.html')

def gantchart(request):
    return render(request, 'pages/gantchart.html')

def dashboard(request):
    return render(request, 'pages/dashboard.html')
