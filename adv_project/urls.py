from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
from . import views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/adv/', include('adventure.urls')),
]
