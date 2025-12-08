from django.urls import path,include
from users.views import *
urlpatterns = [
    path("",show_default),
    path("sign-up/",sign_up, name="sign-up"),
    path("sign-in/",sign_in, name="sign-in")
]