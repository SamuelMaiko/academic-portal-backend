import json
from channels.generic.websocket import AsyncWebsocketConsumer

class WriterRevisionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        first_name = self.scope["url_route"]["kwargs"]["first_name"]
        last_name = self.scope["url_route"]["kwargs"]["last_name"]
        self.group_name=f"{first_name}_{last_name}".lower()

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def revision_add(self, event):
        revision=event["data"]
        await self.send(text_data=json.dumps({"action":"add", "revision":revision}))
    
    async def revision_update(self, event):
        revision=event["data"]
        await self.send(text_data=json.dumps({"action":"update", "revision":revision}))