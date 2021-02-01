from django.urls import path, include

from .api import views

urlpatterns = [
    path('api/', include('apps.demanda.api.urls')),
]
