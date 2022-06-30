from pydoc import visiblename
from unicodedata import name
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('roomlogin/', views.ChatRoomLogin.as_view(), name='room_login'),
    path('chat/room/<int:room_id>', views.ChatRoom.as_view(), name='chat_room')
]
