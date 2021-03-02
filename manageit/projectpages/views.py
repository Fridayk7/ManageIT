from django.shortcuts import render
from projects.models import Project,WBS,Task,TaskRel,TaskUserActivity,ProjectEmployeeRole
import json
import datetime

def activity(request):
    return render(request, 'projectpages/activity.html')

def list(request, project_id):
    wbs = WBS.objects.filter(project__id=project_id)
    tasks = Task.objects.filter(wbs__project__id=project_id)

    context = {
        "project_id": project_id,
        "wbs_list": wbs,
        "task_list": tasks}
    return render(request, 'projectpages/list.html', context)

def kanban(request, project_id):
    wbs = WBS.objects.filter(project__id=project_id)
    nostate = Task.objects.filter(wbs__project__id=project_id,state="nostate")
    todo = Task.objects.filter(wbs__project__id=project_id,state="todo")
    inprogress = Task.objects.filter(wbs__project__id=project_id,state="inprogress")
    completed = Task.objects.filter(wbs__project__id=project_id,state="completed")

    context = {"project_id": project_id,
               "nostate_list": nostate,
               "todo_list": todo,
               "inprogress_list": inprogress,
               "completed_list": completed}
    return render(request, 'projectpages/kanban.html', context)

def gantchart(request, project_id):
    context = {
        "project_id": project_id
    }
    return render(request, 'projectpages/gantchart.html', context)

def dashboard(request, project_id):
    # Log(n)
    wbs = WBS.objects.filter(project__id=project_id)
    tasks = Task.objects.filter(wbs__project__id=project_id)
    profiles = ProjectEmployeeRole.objects.filter(project_id=project_id)
    users_tasks = {}
    for profile in profiles:
        user_to_do = tasks.filter(user__id=profile.user.id).filter(state="todo")
        user_in_progress = tasks.filter(user__id=profile.user.id).filter(state="inprogress")
        user_completed = tasks.filter(user__id=profile.user.id).filter(state="completed")
        users_tasks[str(profile.user)] = [len(user_to_do),len(user_in_progress),len(user_completed)]

    activities = TaskUserActivity.objects.filter(task__wbs__project__id = project_id)
    journey = {}
    wbs_progress = {}
    ids = []

    for n in wbs:
        wbs_tasks_total = tasks.filter(wbs__id=n.id)
        wbs_tasks_completed = wbs_tasks_total.filter(state="completed")
        wbs_progress[n.id] = [len(wbs_tasks_total), len(wbs_tasks_completed)]
        ids.append(n.id)

    if tasks.order_by('start') and tasks.order_by('-end') and activities.order_by('date'):
        earliest_start_date = tasks.order_by('start')[0].start
        latest_end_date = tasks.order_by('-end')[0].end
        earliest_creation_date = activities.order_by('date')[0].date

        delta = datetime.timedelta(days=1)

        total_completed = 0
        total_not_completed = 0
        flag = False

        while earliest_start_date <= latest_end_date:
            if earliest_creation_date <= earliest_start_date and flag == False:
                flag = True
                today = activities.filter(date__lte=earliest_start_date)
            else:
                today = activities.filter(date=earliest_start_date)

            completed_new = len(today.filter(taskstate="completed").filter(action="new"))
            not_completed_new = len(today.exclude(taskstate="completed").filter(action="new"))
            completed_edit = len(today.filter(taskstate="completed").filter(action="edit"))
            not_completed_edit = len(today.exclude(taskstate="completed").filter(action="edit"))
            completed_del = len(today.filter(taskstate="completed").filter(action="del"))
            not_completed_del = len(today.exclude(taskstate="completed").filter(action="del"))

            total_completed = total_completed + completed_new - not_completed_edit - completed_del
            total_not_completed = total_not_completed + not_completed_new - completed_edit - not_completed_del

            journey[earliest_start_date.strftime("%m/%d/%Y")] = [total_not_completed, total_completed]

            earliest_start_date += delta

    nostate = len(tasks.filter(state=None))
    todo = len(tasks.filter(state="todo"))
    inprogress = len(tasks.filter(state="inprogress"))
    completed = len(tasks.filter(state="completed"))

    nostate_JSON = json.dumps(nostate)
    todo_JSON = json.dumps(todo)
    inprogress_JSON = json.dumps(inprogress)
    completed_JSON = json.dumps(completed)
    journey_JSON = json.dumps(journey)
    wbs_progress_JSON = json.dumps(wbs_progress)
    users_tasks_JSON = json.dumps(users_tasks)

    context= {
        "project_id": project_id,
        "nostate": nostate_JSON,
        "todo": todo_JSON,
        "inprogress": inprogress_JSON,
        "completed": completed_JSON,
        "journey": journey_JSON,
        "wbs_progress": wbs_progress_JSON,
        "wbs_ids": ids,
        "users_tasks": users_tasks_JSON
    }
    return render(request, 'projectpages/dashboard.html', context)
