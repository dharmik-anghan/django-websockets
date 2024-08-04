import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync


class MyWebSocketConsumer(WebsocketConsumer):

    def connect(self):
        print("WebSocket connected...")
        print("Channel layer",self.channel_layer)
        print("Channel name",self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        print("Group name", self.group_name)
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        print("Message received from client...", text_data)
        data = json.loads(text_data)
        message = data['message']
        print("Data...", message)
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, 
            {
                "type" : "chat.message",
                "message" : message
            }
            )
    def chat_message(self, event):
        print("Event chat_message", event)
        print("Event type chat_message", type(event))
        # data = json.loads(event)['message']
        self.send(event['message'])

    def disconnect(self, code):
        print("WebSocket disconnected...")
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("WebSocket connected...")
        print("Channel layer",self.channel_layer)
        print("Channel name",self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        print("Group name", self.group_name)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        print("Message received from client...", text_data)
        # await self.send(text_data="Message from async websocket consumer server to client")
        # self.close(code=4122)
        data = json.loads(text_data)
        message = data['message']
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type" : "chat.message",
                "message" : message
            }
        )
    
    async def chat_message(self, event):
        await self.send(event['message'])


    async def disconnect(self, code):
        print("WebSocket disconnected...")
        self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )