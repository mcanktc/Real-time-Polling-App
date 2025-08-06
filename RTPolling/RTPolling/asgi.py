"""
ASGI config for RTPolling project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""
# RTPolling/asgi.py
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import rtpapp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RTPolling.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            rtpapp.routing.websocket_urlpatterns  
        )
    ),
})
