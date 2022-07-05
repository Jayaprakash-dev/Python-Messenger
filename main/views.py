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
        _chat_members = {}
        _is_host = None
        
        for key in redis_client.scan_iter(room_name[0] + '*'):

            if key.decode() == room_name:
                username = req.user.username.title()
                
                if redis_client.hget(room_name, 'host') != None:
                    if  username == redis_client.hget(room_name, 'host').decode():
                        _is_host = True
                    
                for key in redis_client.hkeys(room_name):
                    if key.decode() == 'host' or key.decode() == 'password':
                        continue
                        
                    _chat_members[key.decode()] = redis_client.hget(room_name, key.decode())

                return render(req, 'main/main.html', {'room_name': room_name, 
                                                    'username': username, 
                                                    'chat_members': _chat_members,
                                                    'is_host': _is_host,
                                                    })
            
        return HttpResponseRedirect(reverse('main:home'))


class HomePage(LoginRequiredMixin, View):
    login_url = 'userauthentication:login'
    redirect_field_name = 'redirect_to'
    
    def get(self, req):
        username = req.user.username
        return render(req, 'main/home.html', {'username': username})

    def post(self, req):
        _room = False

        username = req.user.username
        room_name = req.POST.get("room-name")
        password = req.POST.get('password')
        room_type = req.POST.get('room_type')
        
        if room_type == 'c':

            for key in redis_client.scan_iter(room_name[0] + '*'):

                if key.decode() == room_name:
                    return render(req, 'main/home.html', {'msg': 'room name already taken',
                                                          'username': username})

            redis_client.hset(room_name, 'password', password)
            return HttpResponseRedirect(reverse('main:chat_room', kwargs={'room_name': room_name}))
                

        elif room_type == 'j':

            for key in redis_client.scan_iter(room_name[0] + '*'):
                
                if key.decode() == room_name:
                    room_password = redis_client.hget(room_name, 'password')
                    room_password = room_password.decode()
                    
                    if password == room_password:
                        return HttpResponseRedirect(reverse('main:chat_room', kwargs={'room_name': room_name}))
                    else:
                        return render(req, 'main/home.html', {'msg': 'Invalid password',
                                                              'username': username})       
            
            return render(req, 'main/home.html', {'msg': 'specified room is not available, Invalid room_name', 'username': username})
                