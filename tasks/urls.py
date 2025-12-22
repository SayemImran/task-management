from django.urls import path, include
from tasks.views import *

urlpatterns = [
    path("", onload),
    path("home/", home),
    path("user-dashboard/", userdashboard),
    path("manager-dashboard/", managerdashboard, name="manager-dashboard"),
    path("create-task/", create_task, name="create-task"),
    path("update-task/<int:task_id>/", update_task, name="update-task"),
    path("delete-task/<int:task_id>/", delete_task, name="delete-task"),
]
