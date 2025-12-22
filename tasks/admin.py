from django.contrib import admin
from tasks.models import Project, Employee, Tasks, TaskDetail

admin.site.register(Project)
admin.site.register(Employee)
admin.site.register(Tasks)
admin.site.register(TaskDetail)