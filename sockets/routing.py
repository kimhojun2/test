from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('', consumers.ConnectConsumer.as_asgi()),
    path("ws/disconnect/", consumers.DisconnectConsumer.as_asgi()),
    path("ws/send_data/", consumers.SendDataConsumer.as_asgi()),
    re_path(r'ws/connect/$', consumers.MyConsumer.as_asgi()),
]