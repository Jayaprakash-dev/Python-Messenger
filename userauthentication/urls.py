from django.urls import path

from . import views

app_name = 'userauthentication'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('signup/', views.UserSignUpView.as_view(), name='signup'),
    path('logout/', views.logout_user, name='logout')
]
