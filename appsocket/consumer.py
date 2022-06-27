import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer

class Consumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']

        print('room_id: ', self.room_id)

        await self.channel_layer.group_add(self.room_id, self.channel_name)

        await self.accept()
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_id, self.channel_name)

        raise StopConsumer()