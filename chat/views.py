# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
from . import models
import json

def index(request):
    current_user = {}
    current_user['user_name'] = request.user.username
    current_user['is_authenticated'] = str(request.user.is_authenticated)
    return render(request, 'chat/index.html',current_user)
    

def room(request,room_name):
    current_user = {}
    current_user['user_name'] = mark_safe(json.dumps(request.user.username))
    current_user['room_name'] = mark_safe(json.dumps(room_name))
    current_user['is_authenticated'] = str(request.user.is_authenticated)
    #room = models.Room.objects.create(current_user['room_name'])
    return render(request,'chat/room.html',
        current_user)

