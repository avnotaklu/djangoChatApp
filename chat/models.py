from django.http import HttpRequest
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.db import models
import json


User = get_user_model()
request = HttpRequest.body
# Create your models here.
#class Room(models.Model):
#    name = models.TextField(unique=True)
#    def __str__(self):
#        return self.name
class Message(models.Model):
    author = models.ForeignKey(User,related_name='author_messages',on_delete=models.CASCADE)
    room = models.TextField()
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.author.username
    @staticmethod
    def last_10_messages_of_this_room(room_name):
        return Message.objects.filter(room=room_name).order_by('-timestamp').all()[:10]
