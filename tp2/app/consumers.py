import asyncio
import json
from time import sleep
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from app.models import Chat, Group
from channels.db import database_sync_to_async

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket Connected...", event)
        print("Channel Layer...", self.channel_layer) # get default channel layers
        print("Channel Name...", self.channel_name) # get channel name    
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        print("Group name...",self.group_name) # Scope works like scope in django
        # add channel to new existing group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, # group name 
            self.channel_name
            )

        self.send({"type": "websocket.accept"})

    def websocket_receive(self, event):
        print("Message received...", event)
        print("Message received was", event["text"])
        print("Type of message received was", type(event["text"]))
        # self.send({
        #     "type" : "websocket.send",
        #     "text" : "Message sent to client"
        # })
        data = json.loads(event["text"])

        group = Group.objects.get(name=self.group_name)
        if self.scope['user'].is_authenticated:
            # Create new chat
            chat = Chat(content=data['message'], group=group)
            chat.save()
            async_to_sync(self.channel_layer.group_send)(self.group_name, {
                "type" : "chat.message",
                "message" : event['text']
            })
        else:
            self.send({
                "type" : "websocket.send",
                "text" : json.dumps({"message" : "Login required"})
            })
            

    def chat_message(self, event):
        print("Event...", event)
        print("Actuall Data...", event['message'])
        self.send({
            "type" : "websocket.send",
            "text" : event['message']
        })

    def websocket_disconnect(self, event):
        print("Websocket disconnected...", event)
        print("Channel Layer...", self.channel_layer) # get default channel layers
        print("Channel Name...", self.channel_name) # get channel name
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, 
            self.channel_name
        ) 
        raise StopConsumer()
    
class MyAyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Websocket Connected...", event)
        print("Channel Layer...", self.channel_layer) # get default channel layers
        print("Channel Name...", self.channel_name) # get channel name 
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        # add channel to new existing group
        await self.channel_layer.group_add(
            self.group_name, # group name 
            self.channel_name
            )

        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, event):
        print("Message received...", event)
        print("Message received was", event["text"])
        print("Type of message received was", type(event["text"]))
        # self.send({
        #     "type" : "websocket.send",
        #     "text" : "Message sent to client"
        # })

        data = json.loads(event["text"])

        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)

        # Create new chat

        chat = Chat(content=data['message'], group=group)
        await database_sync_to_async(chat.save)()

        await self.channel_layer.group_send(self.group_name, {
            "type" : "chat.message",
            "message" : event['text']
        })

    async def chat_message(self, event):
        print("Event...", event)
        print("Actuall Data...", event['message'])
        await self.send({
            "type" : "websocket.send",
            "text" : event['message']
        })

    async def websocket_disconnect(self, event):
        print("Websocket disconnected...", event)
        print("Channel Layer...", self.channel_layer) # get default channel layers
        print("Channel Name...", self.channel_name) # get channel name
        await self.channel_layer.group_discard(
            self.group_name, 
            self.channel_name
        ) 
        raise StopConsumer()