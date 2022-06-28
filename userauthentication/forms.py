from attr import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserLoginForm(forms.Form):
    pass

class UserRegistraionForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email']

class UserSignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']