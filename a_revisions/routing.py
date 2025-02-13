from django.urls import re_path
from a_revisions.consumers import WriterRevisionConsumer

websocket_urlpatterns = [
    re_path(r"ws/revisions/(?P<first_name>\w+)/(?P<last_name>\w+)/$", WriterRevisionConsumer.as_asgi()),
]
