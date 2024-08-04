from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/wsc/<str:group_name>/", consumers.MyWebSocketConsumer.as_asgi()),    
    path("ws/wac/<str:group_name>/", consumers.MyAsyncWebsocketConsumer.as_asgi()),    
]