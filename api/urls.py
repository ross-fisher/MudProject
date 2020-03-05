from django.urls import include, path
from django.conf.urls import url
import api.api as api
from django.conf.urls import url

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
]
