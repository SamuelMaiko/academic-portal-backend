import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RevisionMessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        revision_id = self.scope["url_route"]["kwargs"]["revision_id"]
        first_name = self.scope["url_route"]["kwargs"]["first_name"]
        self.group_name=f"{revision_id}_{first_name}".lower()

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    async def message_add(self, event):
        message=event["data"]
        # print(message)
        await self.send(text_data=json.dumps({"action":"add", "message":message}))
    async def message_delete(self, event):
        revision_message_id=event["data"]
        # print(message)
        await self.send(text_data=json.dumps({"action":"delete", "message_id":revision_message_id}))
    async def message_read(self, event):
        # print(message)
        await self.send(text_data=json.dumps({"action":"read"}))