from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Project, WBS, Task, TaskRel, TaskUserActivity, ProjectEmployeeRole
from django.contrib.auth.models import User
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .forms import Dependencies
from .utils import check_valid_dates, auto_schedule

@login_required(login_url='accounts-login')
def home(request):
    user_id = request.user.id
    profile = Profile.objects.get(user__id=user_id)
    project_employees = ProjectEmployeeRole.objects.filter(user__id=profile.id)
    context = {
        'projects': project_employees
    }

    return render(request, 'projects/projects.html', context)


@login_required(login_url='accounts-login')
def project(request, project_id):
    project = Project.objects.get(id=project_id)
    wbss = WBS.objects.filter(project__id=project_id).filter(active=True)
    tasks = Task.objects.filter(wbs__project__id=project_id).filter(active=True)
    managers = ProjectEmployeeRole.objects.filter(project__id=project_id).filter(user_role = ProjectEmployeeRole.MANAGER)
    staff = ProjectEmployeeRole.objects.filter(project__id=project_id).filter(user_role=ProjectEmployeeRole.STAFF)
    users = managers | staff
    for manager in managers:
        print (manager.user)
    link = 'https://manage--it.herokuapp.com/'+Profile.objects.get(user__id=request.user.id).code+ '.'+ Project.objects.get(id=project_id).code
    context = {
        "project_id": project_id,
        "project_name": project.name,
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
        if start_date > end_date:
            messages.error(request, f"End date must be set later that the start date")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        wbs_id = request.POST['wbs_id']
        state = request.POST['state']
        profile_id = request.POST['profile_id']

        if wbs_id != "Null":
            wbs = WBS.objects.get(pk=wbs_id)
        else:
            wbs = None
        if profile_id != "Null":
            user = Profile.objects.get(id=profile_id)     # test-fc09d43c40b7
        else:
            user = None
        if state == "Null":
            state = "todo"
        task = Task(name=task_name, start=start_date, end=end_date, wbs=wbs, state=state, user=user)
        task.save()

        task_dep_id = request.POST.getlist("task_id")

        check_result = check_valid_dates(task, start_date, task_dep_id)
        if check_result["success"]:
            if "Null" not in task_dep_id:
                for i in task_dep_id:
                    task_dep = Task.objects.get(pk=i)
                    dep = TaskRel(source=task_dep, target=task)
                    dep.save()
        else:
            for message in check_result["messages"]:
                messages.error(request, f"%s" % message)

        activity = TaskUserActivity(task=task, taskstate=state, action="new")
        activity.save()

        messages.success ( request, "Task created successfully")

        return redirect("/projects/"+project_id)
    return render(request, 'projects/project.html')


@login_required(login_url='accounts-login')
def create_wbs(request):
    if request.method == 'POST':
        project_id = request.POST['project_id']
        wbs_name = request.POST['wbs_name']
        if WBS.objects.filter(project_id=project_id).filter(active=True).filter(name=wbs_name):
            messages.error(request, f"The name of a wbs must be unique")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        parent_id = request.POST['parent_wbs']
        if parent_id != "Null":
            parent = WBS.objects.get(pk=parent_id)
        else:
            parent = WBS.objects.get(project__id=project_id, is_root=True)

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

        root_wbs = WBS(name="Root_"+name, project=project, is_root=True)
        root_wbs.save()

        userid = request.POST['user_id']
        user = Profile.objects.get(user__id=userid)

        project_employee = ProjectEmployeeRole(project=project, user=user, user_role='Manager')
        project_employee.save()
        messages.success (request, "Project created successfully")

    return redirect("/projects/")


@login_required(login_url='accounts-login')
def invite_team(request):
    if request.method == 'POST':
        user_username = request.POST['user_username']
        current_user = request.user
        project_id = request.POST['project_id']
        link = 'https://manage--it.herokuapp.com/' + Profile.objects.get(
            user__id=request.user.id).code + '.' + Project.objects.get(id=project_id).code

        # print(link)
        # print('0')
        if user_username != '':
            user_email = Profile.objects.get(user__username=user_username).user.email
            recipient_name = Profile.objects.get(user__username=user_username).user.first_name
            template = render_to_string('projects/email_template.html',
                                    {'receiver_name': recipient_name, 'link': link,
                                     'sender_name': current_user.first_name})

            email = EmailMessage(
                'You are invited to join a team project.',
                template,
                settings.EMAIL_HOST_USER,
                [user_email],
            )

            # print(user_username)
            # print('1')
            # print(user_email)
            # print(recipient_name)
            # print(current_user)
            # print(project_id)

            email.fail_silently = False
            email.send()

        else:
            user_email = request.POST['user_email']
            recipient_name = ''
            template = render_to_string('projects/email_template.html',
                                    {'receiver_name': recipient_name, 'link': link,
                                     'sender_name': current_user.first_name})

            email = EmailMessage(
                'You are invited to join a team project.',
                template,
                settings.EMAIL_HOST_USER,
                [user_email],
            )

            # print(user_email)
            # print(current_user)
            # print(project_id)

            email.fail_silently = False
            email.send()

        return redirect("/projects/" + project_id)
    return render(request, 'projects/project.html')
