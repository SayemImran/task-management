from django.contrib import admin
from tasks.models import Project, Tasks, TaskDetail

admin.site.register(Project)
admin.site.register(Tasks)
admin.site.register(TaskDetail)