from django.shortcuts import render, redirect, HttpResponseRedirect
from projects.models import Project, WBS, Task, TaskRel, TaskUserActivity, ProjectEmployeeRole
from accounts.models import Profile
from django.contrib import messages
from projects.utils import auto_schedule, check_valid_dates
import json
import datetime

def activity(request):
    return render(request, 'projectpages/activity.html')

def wbs(request, project_id):
    wbss = WBS.objects.filter(project__id=project_id).filter(active=True)
    root = wbss.get(is_root = True)
    project = Project.objects.get(id=project_id)
    structure = project.structure()
    structure_json = json.dumps(structure)
    context = {
        "wbss": wbss,
        "root": root,
        "structure":structure_json,
        "project_id": project_id,
    }
    return render(request, 'projectpages/wbs.html', context)

def delete_wbs(request, project_id):
    if request.method == 'POST':
        wbs_id = request.POST['delete']
        wbs = WBS.objects.get(id=wbs_id)
        children_wbs = wbs.all_wbs()
        children_wbs.append(wbs)
        for child_wbs in children_wbs:
            child_wbs.active = False
            child_wbs.save()
            for task in child_wbs.tasks():
                task.active = False
                task.save()
                activity = TaskUserActivity(task=task, taskstate=task.state, action="del")
                activity.save()
                dependencies = TaskRel.objects.filter(source__wbs__project__id=project_id)
                dependencies.filter(source=task).delete()
                dependencies.filter(target=task).delete()
        wbs.active = False
        wbs.save()
        project = str(project_id)
        return redirect("/projects/" + project + "/wbs")
    return render(request,'projectpages/list.html')

def update_wbs(request, project_id):
    if request.method == 'POST':
        name = request.POST['wbs_name']
        if WBS.objects.filter(project_id=project_id).filter(name=name):
            messages.error(request, f"The name of a wbs must be unique")
            return redirect("/projects/" + str(project_id) + "/wbs")
        wbs_id = request.POST['wbs_id']
        wbs = WBS.objects.get(id=wbs_id)
        wbs.name = name
        if "parent" in request.POST:
            parent = request.POST['parent']
            if parent != "Null":
                parent_wbs = WBS.objects.get(id = parent)
                wbs.parent = parent_wbs
        wbs.save()
        project = str(project_id)
        return redirect("/projects/" + project + "/wbs")
    return render(request,'projectpages/list.html')

def list(request, project_id):
    wbs = WBS.objects.filter(project__id=project_id).filter(active=True)
    tasks = Task.objects.filter(wbs__project__id=project_id).filter(active=True).order_by('start')
    project = Project.objects.get(id=project_id)
    dep = TaskRel.objects.filter(source__wbs__project__id = project_id)
    dependencies = {}
    for i in dep:
        if i.target.active:
            dependencies[i.target.id] = []
    for i in dep:
        if i.target.active and i.source.active:
            dependencies[i.target.id].append([i.source.id])
    dependencies_JSON = json.dumps(dependencies)
    managers = ProjectEmployeeRole.objects.filter(project__id=project_id).filter(user_role = ProjectEmployeeRole.MANAGER)
    staff = ProjectEmployeeRole.objects.filter(project__id=project_id).filter(user_role=ProjectEmployeeRole.STAFF)
    users = managers | staff
    states = []
    states.append("todo")
    states.append("inprogress")
    states.append("completed")
    context = {
        "project_id": project_id,
        "wbs_list": wbs,
        "task_list": tasks,
        "users": users,
        "states": states,
        "dependencies": dependencies,
        "dep_json": dependencies_JSON
    }
    return render(request, 'projectpages/list.html', context)

def wbs_list(request, project_id):
    wbs = WBS.objects.filter(project__id=project_id).filter(active=True)
    tasks = Task.objects.filter(wbs__project__id=project_id).filter(active=True).order_by('start')
    project = Project.objects.get(id=project_id)
    dep = TaskRel.objects.filter(source__wbs__project__id = project_id)
    dependencies = {}
    for i in dep:
        if i.target.active:
            dependencies[i.target.id] = []
    for i in dep:
        if i.target.active and i.source.active:
            dependencies[i.target.id].append([i.source.id])
    dependencies_JSON = json.dumps(dependencies)
    managers = ProjectEmployeeRole.objects.filter(project__id=project_id).filter(user_role = ProjectEmployeeRole.MANAGER)
    staff = ProjectEmployeeRole.objects.filter(project__id=project_id).filter(user_role=ProjectEmployeeRole.STAFF)
    users = managers | staff
    states = []
    states.append("todo")
    states.append("inprogress")
    states.append("completed")
    context = {
        "project_id": project_id,
        "wbs_list": wbs,
        "task_list": tasks,
        "users": users,
        "states": states,
        "dependencies": dependencies,
        "dep_json": dependencies_JSON
    }
    return render(request, 'projectpages/list_wbs.html', context)

def delete_task(request, project_id):
    if request.method == 'POST':
        task = request.POST['delete']
        task = Task.objects.get(id=task)
        task.active = False
        task.save()
        activity = TaskUserActivity(task=task, taskstate=task.state, action="del")
        activity.save()
        dependencies = TaskRel.objects.filter(source__wbs__project__id=project_id)
        dependencies.filter(source=task).delete()
        dependencies.filter(target=task).delete()
        project = str(project_id)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request,'projectpages/list.html')


def update_task(request, project_id):
    tasks = Task.objects.filter(wbs__project__id=project_id)
    if request.method == 'POST':
        name = request.POST['task_name']
        start = request.POST['start_date']
        end = request.POST['end_date']
        if end < start:
            messages.error(request, f"End date must be set later that the start date")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        wbs = request.POST['wbs_id']
        state = request.POST['state']
        task_id = request.POST['task_id']
        assignee = request.POST['assignee']
        project = request.POST['project']
        task_dep_id = request.POST.getlist("dependency")
        task = tasks.get(id=task_id)
        task.name = name
        task.start = start
        task.end = end
        check_result = check_valid_dates(task, start, task_dep_id)
        if check_result["success"]:
            dependents = TaskRel.objects.filter(target=task)
            dependents.delete()
            if task_dep_id:
                if task_dep_id[0] != "Null":
                    for i in task_dep_id:
                        dep_task = tasks.get(id=i)
                        if dep_task.end <= datetime.datetime.strptime(task.start, "%Y-%m-%d").date():
                            dep = TaskRel(source=tasks.get(id=i), target=task)
                            dep.save()
                        else:
                            messages.error(request, f"Dependency constraint prevents link from task: " + str(dep_task)
                                           + " to task: " + str(task))
            for message in auto_schedule(task, end)["messages"]:
                messages.error(request, f"%s" % message)
            if wbs != "Null":
                task.wbs = WBS.objects.get(id=wbs)
            else:
                task.wbs = None
            if assignee != "Null":
                task.user = Profile.objects.get(id=assignee)
            else:
                task.user = None
            if state == "Null":
                state = "todo"
            if task.state != state:
                if task.state == "completed" or state == "completed":
                    activity = TaskUserActivity(task=task, taskstate=state, action="edit")
                    activity.save()
                task.state = state
            task.save()
        else:
            for message in check_result["messages"]:
                messages.error(request, f"%s" % message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request,'projectpages/list.html')

def gantchart(request, project_id):
    critical_tasks = Project.objects.get(id=project_id).critical_activities()
    tasks = Task.objects.filter(wbs__project__id = project_id).filter(active=True)
    dependencies = TaskRel.objects.filter(source__wbs__project__id = project_id)
    dictionary = {}
    for el in tasks:
        dep_array = []
        for i in dependencies.filter(target = el):
            dep_array.append(i.source.id)
        dictionary[el.id] = {"name": el.name, "start_date": str(el.start), "end_date": str(el.end), "id": el.id, "dep":dep_array}
    task_json = json.dumps(dictionary)
    context = {
        "project_id": project_id,
        "tasks": task_json,
        "critical_tasks": critical_tasks
    }
    return render(request, 'projectpages/gantchart.html', context)

def dashboard(request, project_id):
    # Log(n)
    wbs = WBS.objects.filter(project__id=project_id).filter(active=True)
    tasks_unfiltered = Task.objects.filter(wbs__project__id=project_id)
    tasks = tasks_unfiltered.filter(active=True)
    profiles = ProjectEmployeeRole.objects.filter(project_id=project_id)
    users_tasks = {}

    # Workload
    for profile in profiles:
        user_to_do = tasks.filter(user__id=profile.user.id).filter(state="todo")
        user_in_progress = tasks.filter(user__id=profile.user.id).filter(state="inprogress")
        user_completed = tasks.filter(user__id=profile.user.id).filter(state="completed")
        users_tasks[str(profile.user)] = [len(user_to_do),len(user_in_progress),len(user_completed)]

    activities = TaskUserActivity.objects.filter(task__wbs__project__id = project_id)
    journey = {}
    wbs_progress = Project.objects.get(id=project_id).progress()
    ids = []

    for n in wbs:
        ids.append(n.id)

    # Release Burndown
    if tasks_unfiltered.order_by('start') and tasks_unfiltered.order_by('-end') and activities.order_by('date'):
        earliest_creation_date = activities.order_by('date')[0].date
        date_today = datetime.date.today()
        delta = datetime.timedelta(days=1)
        total_completed = 0
        total_not_completed = 0
        flag = False

        while earliest_creation_date <= date_today:
            today = activities.filter(date=earliest_creation_date)

            # Foe each day in the project, we calculate the total number of completed and incomplete tasks
            completed_new = len(today.filter(taskstate="completed").filter(action="new"))
            not_completed_new = len(today.exclude(taskstate="completed").filter(action="new"))
            completed_edit = len(today.filter(taskstate="completed").filter(action="edit"))
            not_completed_edit = len(today.exclude(taskstate="completed").filter(action="edit"))
            completed_del = len(today.filter(taskstate="completed").filter(action="del"))
            not_completed_del = len(today.exclude(taskstate="completed").filter(action="del"))

            total_completed = total_completed + completed_new + completed_edit - not_completed_edit - completed_del
            total_not_completed = total_not_completed + not_completed_new + not_completed_edit - completed_edit - not_completed_del

            # Key: Date, Value: Completed/Not completed tasks
            journey[earliest_creation_date.strftime("%m/%d/%Y")] = [total_not_completed, total_completed]

            earliest_creation_date += delta

    # Tasks Pie Chart
    nostate = len(tasks.filter(state=None))
    todo = len(tasks.filter(state="todo"))
    inprogress = len(tasks.filter(state="inprogress"))
    completed = len(tasks.filter(state="completed"))

    # Json Serialization
    nostate_JSON = json.dumps(nostate)
    todo_JSON = json.dumps(todo)
    inprogress_JSON = json.dumps(inprogress)
    completed_JSON = json.dumps(completed)
    journey_JSON = json.dumps(journey)
    users_tasks_JSON = json.dumps(users_tasks)
    progress_JSON = json.dumps(wbs_progress)

    context= {
        "project_id": project_id,
        "nostate": nostate_JSON,
        "todo": todo_JSON,
        "inprogress": inprogress_JSON,
        "completed": completed_JSON,
        "journey": journey_JSON,
        "wbs_ids": ids,
        "users_tasks": users_tasks_JSON,
        "wbs_progress": progress_JSON
    }
    return render(request, 'projectpages/dashboard.html', context)
