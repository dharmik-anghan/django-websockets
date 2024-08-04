from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from app.models import Group, Chat
from app.serializers import ChatSerializer


# Create your views here.
def index(request, group_name):
    group = Group.objects.filter(name=group_name).first()
    chats = []
    if group:
        chats = Chat.objects.filter(group=group).all()
    else:
        group = Group(name= group_name)
        group.save()
        return HttpResponse("hi")
    return HttpResponse(str(ChatSerializer(chats, many=True).data)
    )