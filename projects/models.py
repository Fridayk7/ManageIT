from django.db import models
from django.utils.timezone import now
from accounts.models import Profile
from .utils import generate_ref_code
from django.conf import settings
from datetime import datetime
from itertools import chain
import pandas as pd
import numpy as np
import datetime



class Project(models.Model):
    name = models.CharField(max_length=60)
    code = models.CharField(max_length=12, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)

    def structure(self):
        # Performs BFS on the project data and returns a data structure which represents the project's wbs hierarchy
        # The data structure returned is a dictionary in the form of Key: WBS ID, VALUE : WBS Contents

        nodes_remaining = WBS.objects.filter(project=self, is_root=True)
        node = nodes_remaining[0].id
        structure = {nodes_remaining[0].id: {}}

        # nodes_remaining is a queue which gets updated everytime a new child is found
        while nodes_remaining:

            # Get next unexplored node in the queue
            current = nodes_remaining[0]
            # children_wbs will contain all other unexplored wbs and it will update the contents of the queue
            children_wbs = nodes_remaining[1:]
            # For every node in the queue we create an entry in the dictionary
            structure[current.id] = {'name': current.name, 'children_wbs': [], 'tasks': {}}
            # Te dictionary's value is updated with the contents of each wbs
            for j in current.children_wbs():
                children_wbs.append(j)
                structure[current.id]['children_wbs'].append(j.id)
            for t in current.tasks():
                structure[current.id]['tasks'][t.id] = t.json()
            nodes_remaining = children_wbs
        return structure

    """
    def structure2(self):
        myData = []
        myDataDict = {}
        wbsDict = {-1 : None}
        for wbs in WBS.objects.filter(project=self):
            parent_id = -1
            if wbs.parent:
                parent_id = wbs.parent.id
            wbsDict[wbs.id] = [parent_id, wbs.name]
        print(wbsDict)

        for task in Task.objects.filter(wbs__project=self):
            wbs_id = task.wbs.id
            wbs_path = str(wbs_id) + "." + str(task.id)
            while wbsDict[wbs_id] is not None:
                print(wbs_id)
                next = wbsDict[wbs_id][0]
                wbs_path = str(next)+"."+wbs_path
                wbs_id = next
            myDataDict[task.id] = {"name": wbs_path}

        for key in myDataDict:
            myData.append(myDataDict[key])

        
        hierarchy = {}

        def find(name, data):
            try:
                node = hierarchy[name]
            except KeyError:
                node = None

            if node is None:
                if data:
                    node = data
                    hierarchy[name] = data
                else:
                    node = {"name": name, "children": []}
                    hierarchy[name] = {"name": name, "children": []}
                if len(name):
                    try:
                        substring = name[0:name.rindex(".")]
                    except ValueError:
                        substring = ""
                    node['parent'] = find(substring, None)
                    node['parent']["children"].append(node)

            return node

        for i in myData:
            find(i['name'], i)

        print (hierarchy)
        return myData
        """

    def progress(self):
        # returns a dictionary that includes the progress(value) of each wbs(key) in a project
        root = WBS.objects.get(project=self, is_root=True)
        # queue included the unexplored nodes
        queue = [root]
        # stack will include all nodes in a BFS order
        stack = []
        progress = {}
        while queue:
            # Loop to create a BFS ordered stack
            root = queue.pop(0)
            stack.append(root)
            root_children = root.children_wbs()
            for i in reversed(root_children):
                queue.append(i)
        for i in reversed(stack):
            # for each node(wbs) in the stack we calculate its duration
            progress[i.id] = {}
            all_tasks = i.tasks()
            completed_tasks = all_tasks.filter(state="completed")
            total_progress = 0
            completed_progress = 0

            # calculate the total duration of the wbs
            for task in all_tasks:
                start = pd.to_datetime(task.start, format="%Y/%m/%d").date()
                end = pd.to_datetime(task.end, format="%Y/%m/%d").date()
                total_progress += np.busday_count(start, end) + 1

            # calculate the amount of time completed
            for task in completed_tasks:
                start = pd.to_datetime(task.start, format="%Y/%m/%d").date()
                end = pd.to_datetime(task.end, format="%Y/%m/%d").date()
                completed_progress += np.busday_count(start, end) + 1

            # add the total and completed time of children wbs's
            for wbs in i.children_wbs():
                total_progress += progress[wbs.id]['total_progress']
                completed_progress += progress[wbs.id]['completed_progress']

            progress[i.id]['total_progress'] = int(total_progress)
            progress[i.id]['completed_progress'] = int(completed_progress)
            progress[i.id]['name'] = i.name

        return progress

    def critical_activities(self):
        project_tasks = Task.objects.filter(wbs__project=self).filter(active=True).order_by('-end')
        task_relationships = TaskRel.objects.filter(source__wbs__project = self, target__wbs__project = self)
        if project_tasks:
            latest = project_tasks[0]
            # Collect all tasks that have the latest date of the project as their end date
            project_tasks = project_tasks.filter(end=latest.end)
            critical_activities = []
            unexplored = []
            for task in project_tasks:
                critical_activities.append(task)
                unexplored.append(task)
            # While there are unexplored tasks, keep traversing the tree
            while unexplored:
                current_task = unexplored.pop(0)
                depend = task_relationships.filter(target=current_task)
                for i in depend:
                    # If condition to decide if task is critical
                    if i.source.end >= current_task.start:
                        critical_activities.append(i.source)
                        unexplored.append(i.source)
        else:
            return []

        return list(set(critical_activities))


class WBS(models.Model):
    name = models.CharField(max_length=60)
    parent = models.ForeignKey("self",  on_delete=models.CASCADE,blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_root = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def children_wbs(self):
        wbs = WBS.objects.filter(parent=self).filter(active=True)
        return wbs

    def tasks(self):
        tasks = Task.objects.filter(wbs=self).filter(active=True)
        return tasks

    def all_wbs(self):
        all_wbs = WBS.objects.filter(project=self.project).filter(active=True)
        queue = [self.id]

        wbs_list = []
        while queue:
            s = queue.pop(0)
            parent = all_wbs.get(id=s)
            for wbs in parent.children_wbs():
                wbs_list.append(all_wbs.get(id=wbs.id))
                queue.append(wbs.id)
        return wbs_list




class Task(models.Model):
    name  = models.CharField(max_length=60)
    start = models.DateField()
    end   = models.DateField()
    wbs   = models.ForeignKey(WBS, on_delete=models.CASCADE, null=True)
    state = models.CharField(max_length=60,blank=True, null=True )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField(default=True)

    def json(self):
        user = self.user
        if user:
            user = user.user.username
        json = {'name': self.name, 'start': str(self.start),'end': str(self.end), 'wbs': self.wbs.id, 'state': self.state,
                'user': user }
        return json

    def __str__(self):
        return self.name


class TaskRel(models.Model):
    source = models.ForeignKey(Task, related_name='source', on_delete=models.CASCADE, blank=True, null=True)
    target = models.ForeignKey(Task, related_name='target', on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)


class TaskUserActivity(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateField(default= now, blank=True)
    taskstate = models.CharField(max_length=60,blank=True, null=True)
    action = models.CharField(max_length=60,blank=True, null=True)

class ProjectEmployeeRole(models.Model):
    STAFF = 'Staff'
    MANAGER = 'Manager'
    USER_ROLE = (
        (STAFF, 'Staff'),
        (MANAGER, 'Manager'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=50, choices=USER_ROLE)

    def __str__(self):
        return self.user_role
