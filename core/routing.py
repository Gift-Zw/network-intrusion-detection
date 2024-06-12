# dashboard/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/network-logs/', consumers.NetworkTrafficConsumer.as_asgi()),
]
