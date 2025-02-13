import json

from channels.generic.websocket import AsyncWebsocketConsumer

class WorkConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name="work"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def work_add(self, event):
        data=event["data"]
        await self.send(text_data=json.dumps({"action":"add", "work":data}))
    async def work_update(self, event):
        data=event["data"]
        await self.send(text_data=json.dumps({"action":"update", "work":data}))
    async def work_delete(self, event):
        # work id
        data=event["data"]
        await self.send(text_data=json.dumps({"action":"delete", "work_id":data}))



    # async def receive(self, text_data):
    #     await self.channel_layer.group_send(
    #         self.group_name,
    #         {
    #             "type": "task.update",
    #             "data": {
    #                 "action": "delete",
    #                 "work": json.loads(text_data),
    #             },
    #         },
    #     )