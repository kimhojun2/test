from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.initialize_socket),
    path('start/', views.socket_client),
    path('send/<str:message>/', views.send_message_to_raspberry),
    path('close/', views.close)
]