import uuid
from django.db.models import Q


def generate_ref_code():
    code = str(uuid.uuid4()).replace("-", "")[:12]
    return code

def check_valid_dates(task, new_start, task_dep_id):
    from .models import Task, Project, TaskRel
    import datetime
    messages = []
    project = Project.objects.get(id=task.wbs.project.id)
    tasks = Task.objects.filter(wbs__project=project).filter(active=True)

    task_rel = TaskRel.objects.filter(source__wbs__project=project, target__wbs__project=project)
    task_rel_target = task_rel.filter(target=task)
    for rel in task_rel_target:
        if rel.source.end > datetime.datetime.strptime(new_start, "%Y-%m-%d").date():
            messages.append("Dependency with task: "+str(rel.source) +
                            " is preventing task: " + str(task) + " from updating")
            return {"success": False, "messages": messages}
    if "Null" not in task_dep_id:
        for task_id in task_dep_id:
            source_task = tasks.get(id=task_id)
            if source_task.end > datetime.datetime.strptime(new_start, "%Y-%m-%d").date():
                messages.append("Dependency with task: " + str(source_task) +
                                " cannot be formed due to inconsistent dates")
                return {"success": False, "messages": messages}
    return {"success": True, "messages": messages}

def auto_schedule(task, new_end):
    from .models import Task, Project, TaskRel
    import datetime

    project = Project.objects.get(id=task.wbs.project.id)
    tasks = Task.objects.filter(wbs__project=project).filter(active=True)
    task_rel = TaskRel.objects.filter(source__wbs__project=project, target__wbs__project=project)
    task_rel_target = task_rel.filter(target=task)
    messages = []

    if tasks:
        unexplored = [task]

        while unexplored:
            current_task = unexplored.pop(0)
            if current_task != task:
                current_end = current_task.end
            else:
                current_end = datetime.datetime.strptime(str(new_end) , "%Y-%m-%d").date()
            depend = task_rel.filter(source=current_task)
            for i in depend:
                if current_end > i.target.start:
                    # move task forward in the schedule while preserving its original duration
                    delta = datetime.timedelta(days= (current_end - i.target.start).days)
                    i.target.start = current_end
                    i.target.end += delta
                    i.target.save()
                    messages.append("Task: " + str(i.target) + "has been rescheduled for " + str(current_end))
                    unexplored.append(i.target)
    else:
        return {"success": True, "messages": messages}

    return {"success": True, "messages": messages}



