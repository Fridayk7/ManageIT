from django.contrib import admin

from .models import Project, Task, WBS, TaskRel, TaskUserActivity

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(WBS)
admin.site.register(TaskRel)
admin.site.register(TaskUserActivity)