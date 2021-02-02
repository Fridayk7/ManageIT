from django.shortcuts import render

def home(request):
    return render(request, 'projects/projects.html')

def project(request):
    return render(request, 'projects/project.html')
