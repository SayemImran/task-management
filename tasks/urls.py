from django.urls import path, include
from tasks.views import home,onload
urlpatterns = [
    path("",onload),
    path("home/",home)
]