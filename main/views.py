import email
import json
from html import escape

import redis
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

redis_client = redis.Redis(host='localhost', port=6379, db=0)


class ChatRoom(LoginRequiredMixin, View):
    login_url = 'userauthentication:login'
    redirect_field_name = 'redirect_to'
    
    def get(self, req, room_name):
        
        for key in redis_client.scan_iter(room_name[0] + '*'):

            if key.decode() == room_name:
                username = req.user.username.title()
                username_char = username[0].upper()
                
                email = req.user.email
                room_name_char = room_name[0].upper()

                return render(req, 'main/main.html', {'room_name': room_name, 
                                                    'username': username, 
                                                    'username_char': username_char, 
                                                    'roomname_char': room_name_char,
                                                    'email': email,
                                                    })
            
            
        return render(req, 'main/home.html', {'message': "Invalid room name, please try again" })


class HomePage(LoginRequiredMixin, View):
    login_url = 'userauthentication:login'
    redirect_field_name = 'redirect_to'
    
    def get(self, req):
        return render(req, 'main/home.html', {'message': ''})

    def post(self, req):

        room_name = req.POST.get("room-name")
        password = req.POST.get('password')
        room_type = req.POST.get('type')
        
        if room_type == 'c':
            for key in redis_client.scan_iter(room_name[0] + '*'):

                if key.decode() == room_name:
                    return render(req, 'main/home.html', {'message': 'room name already taken'})

        elif room_type == 'j':
            
            for key in redis_client.scan_iter(room_name[0] + '*'):
                print('key:', key.decode())
                if key.decode() == room_name:
                    room_password = redis_client.hget(room_name, 'password')
                    room_password = room_password.decode()
                    
                    print(redis_client.hgetall(room_name))
                    
                    if password == room_password:
                        return HttpResponseRedirect(reverse('main:chat_room', kwargs={'room_name': room_name}))
                    else:
                        return render(req, 'main/home.html', {'message': 'Invalid password' })
                
                else:
                    return render(req, 'main/home.html', {'message': 'specified room is not available, Invalid room_name' })


        redis_client.hset(room_name, 'password', password)
        return HttpResponseRedirect(reverse('main:chat_room', kwargs={'room_name': room_name}))