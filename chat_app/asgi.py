"""
ASGI config for chat_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from .urls import websocket_urls

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')

django_http_handler = get_asgi_application()

application=ProtocolTypeRouter({
    'http':django_http_handler,
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urls)

    ))

})
