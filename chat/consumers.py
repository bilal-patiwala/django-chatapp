import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer, JsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import User
from .models import Thread, Message
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("opened")
        user  = self.scope['user']
        print("got user")
        print(user)
        chat_room = f'chat_room{user.id}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(self.chat_room, self.channel_name)
        await self.accept()
        print("accept")

    async def receive(self, text_data=None):
        print("hello receive")
        received_data = json.loads(text_data)
        message = received_data['message']
        sender_username = received_data['sender']
        receiver_username = received_data['receiver']
        thread_id = received_data['thread_id']
        if not message:
            return False

        sender = await self.get_user_object(sender_username)
        receiver = await self.get_user_object(receiver_username)
        thread_obj = await self.get_thread(thread_id)

        if not sender:
            print("error sender not found")

        if not receiver:
            print("error receiver not found")

        if not thread_obj:
            print("error thread obj not found")

        await self.createMessage(thread_obj, sender, message)

        receiver_chat_room = f'chat_room{receiver.id}'
        self_user = self.scope['user']

        response = {
            'message':message,
            'sender':self_user.username,
            'thread_id':thread_id
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

    @database_sync_to_async
    def get_thread(self, thread_id):
        thread = Thread.objects.filter(id=thread_id)
        if thread.exists():
            obj = thread.first()
        else:
            obj = None
        
        return obj

    @database_sync_to_async
    def createMessage(self, thread, user, msg):
        Message.objects.create(message=msg, user=user, thread=thread)

    