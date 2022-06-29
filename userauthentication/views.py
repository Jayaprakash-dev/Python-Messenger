from email import message
import re
from types import NoneType
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

def name_validator(text_data):
    if text_data is None:
        return False
    
    if re.search("^[\w.@+-]+\Z", text_data) is None:
        return False
    

class UserRegisterView(View):

    def get(self, req):
        _registration_form = UserRegistraionForm()
        return render(req, 'userauthentication/userregistration.html', {'form': _registration_form})

    def post(self, req):
        _username = req.POST.get('username')
        _email = req.POST.get('email')
        _submit = False

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
        if _submit:
            User.objects.create_user(username=_username, email=_email)

        return HttpResponseRedirect(reverse('userauthentication:signup'))


class UserSignUpView(View):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pattern = re.compile(reg)

    def get(self, req):
        _signup_form = UserSignupForm()
        return render(req, 'userauthentication/usersignup.html', {'form': _signup_form})

    def post(self, req):

        _username = req.POST.get('username')
        _first_name = req.POST.get('first_name')
        _last_name = req.POST.get('last_name')
        _password_1 = req.POST.get('password1')
        _password_2 = req.POST.get('password2')
        submit = req.POST.get('submit')

        try:
            if name_validator(_first_name) == False and len(_first_name) > 0:
                return JsonResponse({'message': '!name', 'from': 'first'})
            
            if name_validator(_last_name) == False and len(_last_name) > 0:
                return JsonResponse({'message': '!name', 'from': 'last'})
            
            if name_validator(_username) is False and len(_username) > 0:
                return JsonResponse({'message': '!username'})
            
        except Exception:
            if _password_1 != None:
                if re.search(UserSignUpView.pattern, _password_1):
                    message = 'pass_valid'
                        
                    if _password_1 == _password_2:
                        message = 'pass_match'
                        print(message)
                            
                    return JsonResponse({'message': message})
                
                else:
                    return JsonResponse({'message': 'not valid'})
        
        if submit == 'submit':
            User.objects.create_user(
                username=_username,
                password=_password_2,
                first_name=_first_name,
                last_name=_last_name,
            ).save()
            
        return HttpResponseRedirect(reverse('userauthentication:login'))