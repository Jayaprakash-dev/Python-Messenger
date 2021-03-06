from pydoc import visiblename
from unicodedata import name
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('chat/room/<str:room_name>', views.ChatRoom.as_view(), name='chat_room')
]
