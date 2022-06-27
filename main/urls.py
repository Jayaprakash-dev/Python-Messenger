from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('roomlogin/', views.room_login_page, name='room_login')
]
