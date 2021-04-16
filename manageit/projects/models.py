from django.db import models
from django.utils.timezone import now
from accounts.models import Profile
from .utils import generate_ref_code
from django.conf import settings
from datetime import datetime
from itertools import chain
import pandas as pd
import numpy as np


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
        nodes_remaining = WBS.objects.filter(project=self, is_root=True)
        node = nodes_remaining[0].id
        structure = {nodes_remaining[0].id: {}}
        while nodes_remaining:
            children_wbs = []
            for i in nodes_remaining:
                structure[i.id] = {'name': i.name, 'children_wbs': [], 'tasks': {}}
                for j in i.children_wbs():
                    children_wbs.append(j)
                    structure[i.id]['children_wbs'].append(j.id)
                for t in i.tasks():
                    structure[i.id]['tasks'][t.id] = t.json()

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
        root = WBS.objects.get(project=self, is_root=True)
        queue = [root]
        stack = []
        progress = {}
        while queue:
            root = queue.pop(0)
            stack.append(root)
            root_children = root.children_wbs()
            for i in reversed(root_children):
                queue.append(i)
        for i in reversed(stack):
            progress[i.id] = {}
            all_tasks = Task.objects.filter(wbs=i)
            completed_tasks = all_tasks.filter(state="completed")
            total_progress = 0
            completed_progress = 0

            for task in all_tasks:
                start = pd.to_datetime(task.start, format="%Y/%m/%d").date()
                end = pd.to_datetime(task.end, format="%Y/%m/%d").date()
                total_progress += np.busday_count(start, end) + 1

            for task in completed_tasks:
                start = pd.to_datetime(task.start, format="%Y/%m/%d").date()
                end = pd.to_datetime(task.end, format="%Y/%m/%d").date()
                completed_progress += np.busday_count(start, end) + 1

            for wbs in i.children_wbs():
                total_progress += progress[wbs.id]['total_progress']
                completed_progress += progress[wbs.id]['completed_progress']

            progress[i.id]['total_progress'] = total_progress
            progress[i.id]['completed_progress'] = completed_progress
            progress[i.id]['name'] = i.name

        return progress


class WBS(models.Model):
    name = models.CharField(max_length=60)
    parent = models.ForeignKey("self",  on_delete=models.CASCADE,blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_root = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def children_wbs(self):
        wbs = WBS.objects.filter(parent=self)
        return wbs

    def tasks(self):
        tasks = Task.objects.filter(wbs=self)
        return tasks

class Task(models.Model):
    name  = models.CharField(max_length=60)
    start = models.DateField()
    end   = models.DateField()
    wbs   = models.ForeignKey(WBS, on_delete=models.CASCADE, null=True)
    state = models.CharField(max_length=60,blank=True, null=True )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)

    def json(self):
        json = {'name': self.name, 'start': str(self.start),'end': str(self.end), 'wbs': self.wbs.id, 'state': self.state,
                'user': self.user }
        return json

    def __str__(self):
        return self.name


class TaskRel(models.Model):
    Source = models.ForeignKey(Task, related_name='source', on_delete=models.CASCADE, blank=True, null=True)
    Target = models.ForeignKey(Task, related_name='target', on_delete=models.CASCADE, blank=True, null=True)
    Type = models.CharField(max_length=20, blank=True, null=True)


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
