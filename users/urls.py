from django.urls import path,include
from users.views import show_default
urlpatterns = [
    path("",show_default)
]