from django.db import models
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
    wbs   = models.ForeignKey(WBS, on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.name

class TaskRel(models.Model):
    Source = models.ForeignKey(Task, related_name='source', on_delete=models.DO_NOTHING)
    Target = models.ForeignKey(Task, related_name='target', on_delete=models.DO_NOTHING)
    Type = models.CharField(max_length=20)

    def __str__(self):
        return self.Source
