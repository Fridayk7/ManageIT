from django.shortcuts import render, redirect
from .models import Project, WBS, Task, TaskRel, TaskUserActivity, ProjectEmployeeRole
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='accounts-login')
def home(request):
    user_id = request.user.id
    profile = Profile.objects.get(user__id=user_id)
    project_employees = ProjectEmployeeRole.objects.filter(user__id=profile.id)
    print(project_employees)
    context = {
        'projects': project_employees
    }

    return render(request, 'projects/projects.html', context)


@login_required(login_url='accounts-login')
def project(request, project_id):
    wbss = WBS.objects.filter(project__id=project_id)
    tasks = Task.objects.filter(wbs__project__id=project_id)
    managers = ProjectEmployeeRole.objects.filter(project__id=project_id).filter(user_role = ProjectEmployeeRole.MANAGER)
    staff = ProjectEmployeeRole.objects.filter(project__id=project_id).filter(user_role=ProjectEmployeeRole.STAFF)
    users = managers | staff
    link = 'http://127.0.0.1:8000/'+Profile.objects.get(user__id=request.user.id).code+ '.'+ Project.objects.get(id=project_id).code
    context = {
        "project_id": project_id,
        "wbss": wbss,
        "tasks": tasks,
        "managers": managers,
        "staff": staff,
        "users": users,
        "ref_link": link
    }

    return render(request, 'projects/project.html', context)


@login_required(login_url='accounts-login')
def create_task(request):
    if request.method == 'POST':
        project_id = request.POST['project_id']
        task_name = request.POST['task_name']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        wbs_id = request.POST['wbs_id']
        state = request.POST['state']
        profile_id = request.POST['profile_id']
        if wbs_id != "Null":
            wbs = WBS.objects.get(pk=wbs_id)
        else:
            wbs = None
        if profile_id != "Null":
            user = Profile.objects.get(id=profile_id)
        else:
            user = None
        task = Task(name=task_name, start=start_date, end=end_date, wbs=wbs, state=state, user=user)
        task.save()

        task_dep_id = request.POST['task_id']
        dep_type = request.POST['dependency']

        if task_dep_id != "Null" and type != "Null":
            task_dep = Task.objects.get(pk=task_dep_id)
            dep = TaskRel(Source=task_dep, Target=task, Type=dep_type)
            dep.save()

        activity = TaskUserActivity(task=task, taskstate=state, action="new")
        activity.save()

        messages.success ( request, "Task created successfully")

        return redirect("/projects/"+project_id)
    return render(request, 'projects/project.html')


@login_required(login_url='accounts-login')
def create_wbs(request):
    if request.method == 'POST':
        wbs_name = request.POST['wbs_name']
        parent_id = request.POST['parent_wbs']
        if parent_id != "Null":
            parent = WBS.objects.get(pk=parent_id)
        else:
            parent = None
        project_id = request.POST['project_id']
        project = Project.objects.get(pk=project_id)
        wbs = WBS(name=wbs_name, parent=parent, project=project)
        wbs.save()

        messages.success ( request, "Wbs created successfully")

        return redirect("/projects/"+project_id)
    return render(request, 'projects/project.html')


@login_required(login_url='accounts-login')
def create_project(request):
    if request.method == 'POST':
        name = request.POST['project_name']
        project = Project(name=name)
        project.save()

        userid = request.POST['user_id']
        user = Profile.objects.get(user__id=userid)

        project_employee = ProjectEmployeeRole(project=project, user=user, user_role='Manager')
        project_employee.save()
        messages.success (request, "Project created successfully")

    return redirect("/projects/")