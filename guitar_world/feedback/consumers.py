from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat
from auth_app.models import User
from datetime import datetime
import json




class ClientConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def writeMessage(self, user, message):
        chat = Chat.objects.filter(user=user)
        if not chat.exists():
            chat = Chat.objects.create(user=user, messages={f"{user.id}__{datetime.strftime(datetime.now(), '%H:%M:%S')}": message})
            return

        chat = chat.first()

        chat.messages[f"{user.id}__{datetime.strftime(datetime.now(), '%H:%M:%S')}"] = message
        chat.save()

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_client_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.writeMessage(self.scope["user"], message)

        await self.channel_layer.group_send(
            f'chat_admin_{self.room_name}',
            {
                'type': 'chat_message',
                'message': message,
                'sender': 'client',
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))


class AdminConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def writeMessage(self, user, message):
        chat = Chat.objects.filter(user=user)
        if not chat.exists():
            chat = Chat.objects.create(user=user, messages={f"{self.scope['user'].id}__{datetime.strftime(datetime.now(), '%H:%M:%S')}": message})
            return

        chat = chat.first()

        chat.messages[f"{self.scope['user'].id}__{datetime.strftime(datetime.now(), '%H:%M:%S')}"] = message
        chat.save()
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_admin_{self.room_name}'

        if not self.scope['user'].is_authenticated or not self.scope['user'].is_superuser:
            await self.close()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.writeMessage( await sync_to_async(User.objects.get)(id=self.room_name), message)

        await self.channel_layer.group_send(
            f'chat_client_{self.room_name}',
            {
                'type': 'chat_message',
                'message': message,
                'sender': 'admin',
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))