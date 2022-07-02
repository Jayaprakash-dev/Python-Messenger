from bdb import checkfuncname
import json
import asyncio

import redis
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer


rc = redis.Redis(host='localhost', port=6379, db=0)
          

class Consumer(AsyncWebsocketConsumer):

    async def connect(self):
         
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        print('room_id: ', self.room_name)

        await self.channel_layer.group_add(self.room_name, self.channel_name)

        await self.accept()
    
    async def set_room(self):
        for key in rc.scan_iter(str(self.room_name[0]) + '*'):

            if key.decode() == self.room_name:

                if rc.hget(self.room_name, 'host') is None:
                    rc.hset(key.decode(), 'host', self.channel_name)

                else:
                    rc.hset(key.decode(), self.username, self.channel_name)
                    
                    host_channel = rc.hget(self.room_name, 'host').decode()
                    
                    await self.channel_layer.send(host_channel, {
                        'type': 'notification',
                        'user': self.username
                    })
                    
                    # print(rc.hgetall(self.room_name))
            
    async def receive(self, text_data=None):
        
        if text_data != None:
            text_data = json.loads(text_data)
            
            try:
                if text_data.get('username'):
                    self.username = text_data.get('username')
                    
                    loop = asyncio.get_running_loop()
                    await loop.create_task(self.set_room())
                    # response, count, room_name = await loop.create_task(set_room(self.room_name, self.channel_name, self))
            
                    # if response == 'member added':
                    #     host_channel = rc.hget(room_name, 'host').decode()
                    #     await self.channel_layer.send(host_channel, {
                    #         'type': 'notification',
                    #         'message': 'member ' + count + ' added'
                    #     })
                elif text_data.get('ru'):
                    await Consumer.remove_user(self.room_name, text_data.get('ru'), self.channel_name)
                
            except KeyError:
                pass
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        raise StopConsumer()
    
    async def notification(self, event):
        
        username = event.get('user')
        print('sending message')
        
        await self.send(text_data=json.dumps({
            'user': username
        }))

    @staticmethod
    async def remove_user(room_name, username, channel_name):
        
        res = rc.hdel(room_name, username)
        
        if res == 0:
            host_channel = rc.hget(room_name, 'host').decode()

            if host_channel == channel_name:
                rc.hdel(room_name, 'host')
        
        if rc.hlen(room_name) == 1:
            rc.delete(room_name)
        