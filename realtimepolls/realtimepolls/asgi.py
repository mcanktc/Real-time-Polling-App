"""
ASGI config for realtimepolls project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from pollingapp.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtimepolls.settings')

application = ProtocolTypeRouter(
    AuthMiddlewareStack({
        "http" : get_asgi_application(),
        "websocekt" : URLRouter(websocket_urlpatterns)
    })
)
