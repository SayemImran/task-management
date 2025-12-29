# from django.urls import path, include
# from tasks.views import *

# # urlpatterns = [
# #     path("", onload),
# #     path("home/", home),
# #     path("user-dashboard/", userdashboard),
# #     # path("manager-dashboard/", managerdashboard, name="manager-dashboard"),
# #     path("manager-dashboard/", ManagerDashboardView.as_view(), name="manager-dashboard"),
# #     # path("create-task/", create_task, name="create-task"),
# #     path("create-task/", TaskCreateView.as_view(), name="create-task"),
# #     path("update-task/<int:task_id>/", update_task, name="update-task"),
# #     path("delete-task/<int:task_id>/", delete_task, name="delete-task"),

# #     path('task/<int:task_id>/details/',task_details, name='task-details'),
# # ]

from django.urls import path
from tasks.views import (
    HomeView,
    OnloadView,
    UserDashboardView,
    ManagerDashboardView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    path("user-dashboard/", UserDashboardView.as_view(), name="user-dashboard"),
    path("manager-dashboard/", ManagerDashboardView.as_view(), name="manager-dashboard"),

    path("create-task/", TaskCreateView.as_view(), name="create-task"),
    path("update-task/<int:task_id>/", TaskUpdateView.as_view(), name="update-task"),
    path("delete-task/<int:task_id>/", TaskDeleteView.as_view(), name="delete-task"),

    path("task/<int:task_id>/details/", TaskDetailView.as_view(), name="task-details"),
]
