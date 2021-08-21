# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
from . import models
import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
import time

# helper functions 

@database_sync_to_async
def get_user(request):
    return request.user.username

@database_sync_to_async
def messages_to_json(messages):

    result = []
    for message in messages:
        get_messages = message_to_json(message)
        result.append(get_messages)
    return result

def message_to_json(message):
    return {
        'author':message.author.username,
        'content':message.content,
        'timestamp':str(message.timestamp),
        'room':message.room
    }

# views

def index(request):
    current_user = {}
    current_user['user_name'] = request.user.username
    current_user['is_authenticated'] = str(request.user.is_authenticated)
    return render(request, 'chat/index.html',current_user)
    

async def room(request,room_name):

    start_time = time.time()
    queryset_coroutine = models.Message.last_10_messages_of_this_room(room_name)
    qset = await queryset_coroutine

    current_user = {}
    current_user['user_name'] = mark_safe(json.dumps(await get_user(request)))
    current_user['room_name'] = mark_safe(json.dumps(room_name))
    current_user['is_authenticated'] = str(request.user.is_authenticated)
    
    end_time = time.time()
    print(end_time-start_time);
    current_user['messages'] =  mark_safe(json.dumps(await messages_to_json(qset)))

    #room = models.Room.objects.create(current_user['room_name'])

    end_time = time.time()
    print("time elapsed",end_time-start_time);
    return render(request,'chat/room.html', current_user)
