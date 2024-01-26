from django.urls import path, include
from . import views

urlpatterns = [
    path('sockets/', views.socket_client),
    path('close/', views.close)
]