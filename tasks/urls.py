from django.urls import path, include
from tasks.views import home,onload, userdashboard, managerdashboard,create_task
urlpatterns = [
    path("",onload),
    path("home/",home),
    path('user-dashboard/',userdashboard),
    path('manager-dashboard/',managerdashboard),
    path('create-task/',create_task)
]