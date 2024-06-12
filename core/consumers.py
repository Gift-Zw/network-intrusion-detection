# dashboard/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NetworkTrafficConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "network_logs",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "network_logs",
            self.channel_name
        )

    async def send_log(self, event):
        log = event['log']
        await self.send(text_data=json.dumps(log))
