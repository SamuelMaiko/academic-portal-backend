import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django_asgi_app = get_asgi_application()

from a_work.routing import websocket_urlpatterns as work_websockets
from a_revisions.routing import websocket_urlpatterns as revisions_websockets

# Combine the WebSocket URL patterns
combined_websocket_urlpatterns = work_websockets + revisions_websockets

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(combined_websocket_urlpatterns))
        ),
})
