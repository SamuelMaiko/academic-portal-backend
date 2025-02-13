from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_notifications.models import Notification
from a_work.models import Work
from a_work.permissions import IsAdmin
from a_work.serializers import CreateWorkSerializer
from a_work.serializers import WorkSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class CreateWorkView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @swagger_auto_schema(
        operation_description="Creates new work.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'deadline': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Deadline for the work (ISO 8601 date-time format)'),
                'words': openapi.Schema(type=openapi.TYPE_STRING, description='No. of words'),
                'type': openapi.Schema(type=openapi.TYPE_STRING, description='Type of the work'),
                'assigned_to': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID of the person assigned to this work'),
                'comment': openapi.Schema(type=openapi.TYPE_STRING, description='Additional comments or notes')
            },
            required=['deadline', 'words'],
        ),
        responses={
            201: openapi.Response(
                description="Work created successfully",
                examples={
                    "application/json": {
                        "id": 15,
                        "deadline": "2024-07-17T15:00:00+03:00",
                        "work_code": "WK78015",
                        "words": 1500,
                        "type": "Essay",
                        "assigned_to": None,
                        "comment": None
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": {
                        "error": "Invalid data"
                    }
                }
            ),
        },
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
        ],
        tags=['Work']
    )
     
    def post(self, request, *args, **kwargs):
        self.check_object_permissions(request, request.user)
        serializer = CreateWorkSerializer(data=request.data)
        if serializer.is_valid():
            work=serializer.save(author=request.user)
            # print(request.data)
            assigned_to=serializer.validated_data.get("assigned_to", None)

            work_data = WorkSerializer(work, context={"request":request}).data
            # sending to socket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "work",
                {
                    "type": "work.add",
                    "data": work_data,
                }
            )



            if assigned_to is not None:
                # adding a notification
                notification=Notification.objects.create(
                    type="Assigned Work",
                    message="work has been has been assigned",
                    triggered_by=request.user,
                    work=work
                    )
                notification.users.add(assigned_to)
                # Notify admins
                admins=get_admins()
                new_notification=Notification.objects.create(
                    type="System Notification",
                    message="work has been has been assigned",
                    triggered_by=request.user,
                    work=work
                    )
                new_notification.users.add(*admins)
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
