from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/work/", consumers.WorkConsumer.as_asgi()),
]