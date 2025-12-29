from django.contrib import admin
from django.urls import path,include
from core.views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('',include("core.urls")),
    path('users/',include("users.urls")),
    path('admin/', admin.site.urls),
    path('tasks/',include("tasks.urls")),
    path('no-permission/',no_permission, name='no-permission')
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)