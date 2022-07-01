from django.urls import URLPattern, re_path

from . import consumer

websocket_urlpatterns = [
    re_path(r'chat/room/(?P<room_name>\w+)/$', consumer.Consumer.as_asgi()),
]