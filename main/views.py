from audioop import reverse
from html import escape
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse

class ChatRoomLogin(View):

    def get(self, req):
        return render(req, 'main/roomlogin.html')
    
    def post(self, req):
    
        room_id = str(escape(req.POST.get('room-id')))

        return HttpResponseRedirect(reverse('main:chat_room', kwargs={'room_id': room_id}))


class ChatRoom(View):

    def get(self, req, room_id):
        return render(req, 'main/main.html')
 
    
class HomePage(View):
    
    def get(self, req):
        return render(req, 'main/home.html')
    
    def post(self, req):
        pass