from django.urls import URLPattern, re_path

from . import consumer

websocket_urlpatterns = [
    re_path(r'chat/room/(?P<room_id>\w+)/$', consumer.Consumer.as_asgi()),
]