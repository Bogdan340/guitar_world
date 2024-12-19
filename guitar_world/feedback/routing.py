from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/client/<str:room_name>/', consumers.ClientConsumer.as_asgi()),
    path('ws/chat/admin/<str:room_name>/', consumers.AdminConsumer.as_asgi()),
]