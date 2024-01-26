"""
ASGI config for websocket project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from sockets import consumers
import sockets.routing
from django.urls import path


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websocket.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            sockets.routing.websocket_urlpatterns
            # path("ws/connect/", consumers.ConnectConsumer.as_asgi()),
            # path("ws/disconnect/", consumers.DisconnectConsumer.as_asgi()),
            # path("ws/send_data/", consumers.SendDataConsumer.as_asgi()),
        )
    )
})
