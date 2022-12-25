import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user  = self.scope['user']
        chat_room = f'chat_room{user.id}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(self.chat_room, self.channel_name)
        await self.accept()

    async def receive(self, text_data=None):
        received_data = json.loads(text_data)
        message = received_data['message']
        sender_username = received_data['sender']
        receiver_username = received_data['receiver']
        if not message:
            return False

        sender = await self.get_user_object(sender_username)
        receiver = await self.get_user_object(receiver_username)

        if not sender:
            print("error sender not found")

        if not receiver:
            print("error receiver not found")

        receiver_chat_room = f'chat_room{receiver.id}'
        self_user = self.scope['user']

        response = {
            'message':message,
            'sender':self_user.username,
        }

        await self.channel_layer.group_send(
            receiver_chat_room,
            {
                'type':'chat_message',
                'text':json.dumps(response)
            }
        )


        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type':'chat_message',
                'text':json.dumps(response)
            }
        )

        # await self.send(json.dumps({
        #     'type':'websocket.send',
        #     'text':response
        # }))

    async def disconnect(self, code):
        pass

    async def chat_message(self, event):
        message = event["text"]

        await self.send(json.dumps({"text": message}))

    @database_sync_to_async
    def get_user_object(self,username):
        user = User.objects.filter(username=username)
        if user.exists():
            return user.first()
        else:
            return None

    

    