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

        await self.channel_layer.group_add(self.room_name, self.channel_name)

        await self.accept()
    
    async def set_room(self):
        for key in rc.scan_iter(str(self.room_name[0]) + '*'):

            if key.decode() == self.room_name:

                if rc.hget(self.room_name, 'host') is None:
                    rc.hset(key.decode(), 'host', self.username)
                    rc.hset(key.decode(), self.username, self.channel_name)
                    
                    await self.send(text_data=json.dumps({
                            'is_host':  True
                        }))

                else:
                    rc.hset(key.decode(), self.username, self.channel_name)

                    host = rc.hget(self.room_name, 'host').decode()
                    host_channel = rc.hget(key.decode(), host).decode()
                    
                    await self.channel_layer.send(host_channel, {
                        'type': 'notification',
                        'user': self.username
                    })
            
    async def receive(self, text_data=None):
        loop = asyncio.get_running_loop()
        
        if text_data != None:
            text_data = json.loads(text_data)
            
            try:
                if text_data.get('username'):
                    self.username = text_data.get('username')
                    
                    await loop.create_task(self.set_room())

                    # response, count, room_name = await loop.create_task(set_room(self.room_name, self.channel_name, self))
            
                    # if response == 'member added':
                    #     host_channel = rc.hget(room_name, 'host').decode()
                    #     await self.channel_layer.send(host_channel, {
                    #         'type': 'notification',
                    #         'message': 'member ' + count + ' added'
                    #     })
                    
                elif text_data.get('ru'):
                    username = text_data.get('ru')
                    
                    if rc.hlen(self.room_name) > 3:
                        await loop.create_task(self.channel_layer.group_send(self.room_name,
                            {
                                'type': 'remove_user',
                                'user': username
                            }
                        ))
                        await self.channel_layer.group_discard( self.room_name, (rc.hget(self.room_name, username).decode()) )
                    
                    await loop.create_task(Consumer.redis_remove_user(self.room_name, username))
                
                elif text_data.get('req_to_au'):
                    username = text_data.get('req_to_au')
                    
                    await loop.create_task(self.channel_layer.group_send(
                        self.room_name,
                        {
                            'type': 'confirm_user',
                            'user': username
                        }
                    ))
                    
                elif text_data.get('message'):
                    message = text_data.get('message')
                    username = text_data.get('username')
                    
                    await loop.create_task(self.channel_layer.group_send(
                        self.room_name,
                        {
                            'type': 'chat_message',
                            'message': message
                        }
                    ))
                
            except Exception as e:
                print(e)
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        raise StopConsumer()
    
    async def notification(self, event):
        
        username = event.get('user')

        await self.send(text_data=json.dumps({
            'notification': username # au - add user
        }))
    
    async def chat_message(self, event):
        
        await self.send(text_data=json.dumps({
            'message':  event.get('message')
        }))
        
    async def confirm_user(self, event):
        await self.send(text_data=json.dumps({
            'add_user':  event.get('user')
        }))

    @staticmethod
    async def redis_remove_user(room_name, username):

        rc.hdel(room_name, username)
        
        if rc.hlen(room_name) == 2:
            rc.delete(room_name)
    
    async def remove_user(self, event):

        await self.send(text_data=json.dumps({
            'remove_user':  event.get('user')
        }))
        