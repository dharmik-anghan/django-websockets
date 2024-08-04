from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path("ws/sc/<str:group_name>/", consumers.MySyncConsumer.as_asgi()),
    path("ws/ac/<str:group_name>/", consumers.MyAyncConsumer.as_asgi()),
    path("ws/wc/", consumers.MyWebSocketConsumer.as_asgi()),
]