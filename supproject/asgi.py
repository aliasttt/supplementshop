import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from supplementapp.routing import websocket_urlpatterns
# تنظیمات پروژه Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supproject.settings')

# تعریف application که هم درخواست‌های HTTP و هم WebSocket رو پشتیبانی می‌کنه
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # درخواست‌های HTTP
    "websocket": AuthMiddlewareStack(
        URLRouter([
            websocket_urlpatterns
        ])
    ),
})

