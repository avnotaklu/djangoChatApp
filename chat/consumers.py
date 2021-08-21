# chat/consumers.py
from django.contrib.auth import get_user_model
import json
from json import JSONEncoder
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

import datetime
import asyncio
import inspect
import os
import time


User = get_user_model()
class ChatConsumer(AsyncWebsocketConsumer):
    start_time = time.time()
    end_time = time.time()

    @database_sync_to_async
    def get_messages(self):
        # return Message.last_10_messages_of_this_room(self.room_name)
        return Message.objects.filter(room=room_name).order_by('-timestamp').all()

    @database_sync_to_async
    def messages_to_json(self,messages):
        result = []
        for message in messages:
            get_messages = self.message_to_json(message)
            result.append(get_messages)
        self.end_time = time.time()
        return result
    @database_sync_to_async
    def get_username(self,author):
        return User.objects.filter(username=author)[0]
    @database_sync_to_async
    def create_message(self,data,author_user):
        new_message = Message.objects.create(
                author=author_user,
                content=data['message'],
                room=data['room_name']
                )
        return new_message



    

    def message_to_json(self,message):
        return {
            'author':message.author.username,
            'content':message.content,
            'timestamp':str(message.timestamp),
            'room':message.room
        }

    async def fetch_messages(self,_):
        qset_cor = self.get_messages()
        qset = await qset_cor
        
        content = {
            'command': 'fetch_messages',
            'messages' : await self.messages_to_json(qset)
        }

        result = asyncio.create_task(self.send_message(content))
        await result

    async def new_messages(self,data):
        author = data['from']
        author_user = await self.get_username(author)

        message = await self.create_message(data,author_user)

        content = {
            'command': 'new_messages',
            'message': self.message_to_json(message)
            }

        return await self.send_chat_message(content)
    
    commands = {
    'fetch_messages':fetch_messages,
    'new_messages':new_messages
    }

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_message(self,message):
        self.end_time = time.time()
        await self.send(text_data=json.dumps(message))

    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.commands[data['command']](self,data)

    async def send_chat_message(self,message):
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
