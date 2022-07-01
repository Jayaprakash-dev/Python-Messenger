from email import message
import re
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

class UserLoginView(View):

    def get(self, req):
        return render(req, 'userauthentication/userlogin.html', {'message': ''})
    
    def post(self, req):
        _user_input = req.POST.get('user_input')
        _password = req.POST.get('password')
        
        if '@' in _user_input:
            user = authenticate(req, emial=_user_input, password=_password)
        else:
            user = authenticate(req, username=_user_input, password=_password)
            
        if user is None:
            message = "Invalid login details, Please try again"
            return render(req, 'userauthentication/userlogin.html', {'message': message})
        else:
            redirect_url = req.GET.get('redirect_to')
            login(req, user)
            return redirect(redirect_url)

def logout_user(req):
        logout(req)
        return HttpResponseRedirect(reverse('userauthentication:login'))

def name_validator(text_data):
    if text_data is None:
        return False
    
    if re.search("^[\w.@+-]+\Z", text_data) is None:
        return False
    else:
        return True


class UserSignUpView(View):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pattern = re.compile(reg)

    def get(self, req):
        return render(req, 'userauthentication/usersignup.html')

    def post(self, req):

        _username = req.POST.get('username')
        _email = req.POST.get('email')
        _first_name = req.POST.get('first_name')
        _last_name = req.POST.get('last_name')
        _password_1 = req.POST.get('password1')
        _password_2 = req.POST.get('password2')
        submit = req.POST.get('submit')

        try:
            if len(_email) > 0:
                if User.objects.filter(email=_email).exists():
                    return JsonResponse({'message': '!email'})
                
            if name_validator(_first_name) == False and len(_first_name) > 0:
                return JsonResponse({'message': '!name', 'from': 'first'})
            
            if name_validator(_last_name) == False and len(_last_name) > 0:
                return JsonResponse({'message': '!name', 'from': 'last'})
            
            if name_validator(_username) is False and len(_username) > 0:
                return JsonResponse({'message': '!username'})
            
            if User.objects.filter(username=_username).exists():
                return JsonResponse({'message': '!available'})
            
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
                email=_email,
                password=_password_2,
                first_name=_first_name,
                last_name=_last_name,
            ).save()
            
            return HttpResponseRedirect(reverse('userauthentication:login'))
        
        return HttpResponseRedirect(reverse('userauthentication:signup'))