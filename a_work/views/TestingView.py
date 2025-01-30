from rest_framework.response import Response
from rest_framework.views import APIView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class TestingView(APIView):
    permission_classes = []

    def get(self, request):

        work_data = {
            "id": 8,
            "work_code": "WK1508",
            "deadline": "2025-02-17T15:00:00+03:00",
            "words": 2000,
            "type": "Reflection Paper",
            "created_at": "2024-07-17T11:03:54.820923+03:00",
            "is_bookmarked": False,
            "has_writer": False,
            "is_mine": False
        }

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "work",
            {
                "type": "task.update",
                "data": {
                    "action": "add",
                    "work": work_data,
                },
            },
        )

        response=dict(message="Hello just testing things!")
        return Response(response)