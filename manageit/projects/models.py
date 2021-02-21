from django.db import models
from django.utils.timezone import now
from django.conf import settings
from datetime import datetime

class Project(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class WBS(models.Model):
    name = models.CharField(max_length=60)
    parent  = models.ForeignKey("self",  on_delete=models.CASCADE,blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Task(models.Model):
    name  = models.CharField(max_length=60)
    start = models.DateField()
    end   = models.DateField()
    wbs   = models.ForeignKey(WBS, on_delete=models.CASCADE, null=True)
    state = models.CharField(max_length=60,blank=True, null=True )
    
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




