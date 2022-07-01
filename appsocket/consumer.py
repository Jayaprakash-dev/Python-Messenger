import json
import asyncio

import redis
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer


rc = redis.Redis(host='localhost', port=6379, db=0)

# async def set_room(room_name, channel_name, username, socket):
#     for key in rc.scan_iter(str(room_name[0]) + '*'):

#         if key.decode() == room_name:

#             if rc.hget(room_name, 'host') is None:
                
#                 rc.hset(key.decode(), 'host', channel_name)
                
#                 return ('host added', Consumer.count, room_name)

#             else:
#                 rc.hset(key.decode(), username, channel_name)
                
#                 host_channel = rc.hget(room_name, 'host').decode()
                
#                 await socket.channel_layer.send(host_channel, {
#                     'type': 'notification',
#                     'user': username
#                 })
                

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
            
    async def receive(self, text_data=None):
        
        if text_data != None:
            text_data = json.loads(text_data)
            
            try:
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