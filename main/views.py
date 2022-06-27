from django.shortcuts import render
from django.http import HttpResponseRedirect

def room_login_page(req):
    return render(req, 'main/roomlogin.html')