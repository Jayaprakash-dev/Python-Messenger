import re
import redis
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User

from .forms import UserRegistraionForm, UserSignupForm, UserLoginForm

# redis
redis_client = redis.Redis(
    host='127.0.0.1', port=6379
)


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

        # checks username already exists in the database or not
        if User.objects.filter(username=_username).exists():
            data = {'message': "username already taken"}
            return JsonResponse(data)

        # checks the user entered is valid or not with regex pattern
        if len(_username) > 2:
            if re.search("^[\w.@+-]+\Z", _username) is None:
                data = {'message': "username is not valid"}
                return JsonResponse(data)

        # checks the email already exists in the database or not
        if User.objects.filter(email=_email).exists():
            data = {'message': "email is already registered"}
            return JsonResponse(data)

        # if username & email is valid, it will be updated in the redis memeory
        redis_client.set('username', _username)
        redis_client.set('email', _email)

        return HttpResponseRedirect(reverse('userauthentication:signup'))


class UserSignUpView(View):

    def get(self, req):
        initial_data = {
            'username': (redis_client.get('username').decode('utf-8')),
            'email': str(redis_client.get('email').decode('utf-8'))
        }
        _signup_form = UserSignupForm(initial=initial_data)
        return render(req, 'userauthentication/usersignup.html', {'form': _signup_form})

    def post(self, req):

        _first_name = req.POST.get('first_name')
        _last_name = req.POST.get('last_name')
        _password_1 = req.POST.get('password1')
        _password_2 = req.POST.get('password2')

        if len(_first_name) > 0 or len(_last_name) > 0:
            if re.search("^[\w.@+-]+\Z", _first_name) is None:
                data = {'message': "first or last name is not valid"}
                return JsonResponse(data)

            if re.search("^[\w.@+-]+\Z", _last_name) is None:
                data = {'message': "first or last name is not valid"}
                return JsonResponse(data)

        if len(_password_1) >= 8:
            if _password_1 == _password_2:
                
                _signup_form = UserSignupForm(req.POST)
                
                if _signup_form.is_valid():
                    _signup_form.save()

            else:
                data = {'message': "password mismatching"}
                return JsonResponse(data)

        else:
            return JsonResponse({'message': ''})

        return HttpResponseRedirect(reverse('userauthentication:register'))
