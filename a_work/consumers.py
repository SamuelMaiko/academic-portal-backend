import json

from channels.generic.websocket import AsyncWebsocketConsumer

class WorkConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name="work"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "task.update",
                "data": {
                    "action": "delete",
                    "work": json.loads(text_data),
                },
            },
        )

    async def task_update(self, event):
        data=event["data"]
        await self.send(text_data=json.dumps(data))
