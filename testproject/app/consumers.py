import asyncio
from time import sleep
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket Connected...", event)
        print("Channel Layer...", self.channel_layer) # get default channel layers
        print("Channel Name...", self.channel_name) # get channel name 
        print("Scope...", self.scope)
        """
        Scope...
        {
            'type': 'websocket', 
            'path': '/ws/sc/virat/', 
            'raw_path': b'/ws/sc/virat/', 
            'root_path': '', 
            'headers': [
                (b'sec-websocket-version', b'13'), 
                (b'sec-websocket-key', b'uFbEda0FKVTpVxDNa9IG1g=='), 
                (b'connection', b'Upgrade'), (b'upgrade', b'websocket'), 
                (b'sec-websocket-extensions', b'permessage-deflate; client_max_window_bits'), 
                (b'host', b'127.0.0.1:8000')], 
            'query_string': b'', 
            'client': ['127.0.0.1',58757],
            'server': ['127.0.0.1', 8000], 
            'subprotocols': [], 
            'asgi': {'version': '3.0'}, 
            'path_remaining': '', 
            'url_route': {
                'args': (), 
                'kwargs': {'group_name': 'virat'}
                }}
        """

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
        async_to_sync(self.channel_layer.group_send)(self.group_name, {
            "type" : "chat.message",
            "message" : event['text']
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
    
    
# class MySyncConsumer(SyncConsumer):
#     def websocket_connect(self, event):
#         print("Websocket Connected...", event)
#         self.send({"type": "websocket.accept"})

#     def websocket_receive(self, event):
#         print("Message received...", event)
#         print("Message received was", event["text"])
#         # self.send({
#         #     "type" : "websocket.send",
#         #     "text" : "Message sent to client"
#         # })
#         for num in range(51):
#             self.send({"type": "websocket.send", "text": str(num)})
#             sleep(1)

#     def websocket_disconnect(self, event):
#         print("Websocket disconnected...", event)
#         raise StopConsumer()


# class MyAyncConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):
#         print("Websocket Connected...", event)
#         await self.send({"type": "websocket.accept"})

#     async def websocket_receive(self, event):
#         print("Message received...", event)
#         print("Message received was", event["text"])
#         # await self.send({"type": "websocket.send", "text": "Message sent to client"})'
#         for num in range(51):
#             await self.send({"type": "websocket.send", "text": str(num)})
#             await asyncio.sleep(1)


#     async def websocket_disconnect(self, event):
#         print("Websocket disconnected...", event)
#         raise StopConsumer()


class MyWebSocketConsumer(WebsocketConsumer):
    def connect(self):
        print("Generic WebSocketConsumer...")
        print("Generic WebSocketConsumer Connecting...")
        self.connect()
        print("Generic WebSocketConsumer Connected...")
        return super().connect()

    def receive(self, text_data=None, bytes_data=None):
        print("Websocket Recived", text_data)
        return text_data

    def disconnect(self, code):
        return super().disconnect(code)


