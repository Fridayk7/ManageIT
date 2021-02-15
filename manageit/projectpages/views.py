from django.shortcuts import render
from projects.models import Project,WBS,Task,TaskRel

def activity(request):
    return render(request, 'projectpages/activity.html')

def list(request, project_id):
    context = {
        "project_id": project_id
    }
    return render(request, 'projectpages/list.html', context)

def kanban(request, project_id):
    context = {
        "project_id": project_id
    }
    return render(request, 'projectpages/kanban.html', context)

def gantchart(request, project_id):
    context = {
        "project_id": project_id
    }
    return render(request, 'projectpages/gantchart.html', context)

def dashboard(request, project_id):
    context= {
        "project_id": project_id
    }
    return render(request, 'projectpages/dashboard.html', context)

