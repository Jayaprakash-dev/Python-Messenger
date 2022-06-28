import email
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User

from .forms import UserRegistraionForm, UserSignupForm, UserLoginForm

class UserLoginView(View):

    def get(self, req):
        _login_form = UserLoginForm()
        return render(req, 'userauthentication/userlogin.html', {'form': _login_form})


class UserRegisterView(View):

    def get(self, req):
        _registration_form = UserRegistraionForm()
        return render(req, 'userauthentication/userregistration.html', {'form': _registration_form})
    
    def post(self, req):
        _username = req.POST.get('username')
        _email = req.POST.get('email')

        if User.objects.filter(username=_username).exists():
            data = {'message': "username already taken"}
            return JsonResponse(data)
        
        if User.objects.filter(email=_email).exists():
            data = {'message': "email is already registered"}
            return JsonResponse(data)

        return HttpResponseRedirect(reverse('userauthentication:signup'))


class UserSignUpView(View):

    def get(self, req):
        _signup_form = UserSignupForm()
        return render(req, 'userauthentication/usersignup.html', {'form': _signup_form})

    def post(self, req):
        _password_1 = req.POST.get('password1')
        _password_2 = req.POST.get('password2')

        if _password_1 == _password_2:
            _registration_form = UserSignupForm(req.POST)
            data = {'message': "password correct"}
            JsonResponse(data)

            if _registration_form.is_valid():
                _registration_form.save()
            else:
                print(_registration_form.errors.as_data())
        else:
            data = {'message': "password mismatching"}
            return JsonResponse(data)
        
        return HttpResponseRedirect(reverse('userauthentication:register'))