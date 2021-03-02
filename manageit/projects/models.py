from django.db import models
from django.utils.timezone import now
from accounts.models import Profile
from .utils import generate_ref_code
from django.conf import settings
from datetime import datetime


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
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    
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
