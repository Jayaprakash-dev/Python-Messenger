from django.urls import path

from . import views

app_name = 'userauthentication'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('signup/', views.UserSignUpView.as_view(), name='signup')
]
