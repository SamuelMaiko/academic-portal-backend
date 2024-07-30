from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_notifications.serializers import NotificationSerializer


class NotificationsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieve notifications for the authenticated user.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="OK",
                examples={
                    "application/json": [
                        {
                            "id": 46,
                            "message": "work has been has been uptaken",
                            "type": "Uptaken Work",
                            "triggered_by": {
                                "id": 1,
                                "registration_number": "TW9801",
                                "first_name": "Sam",
                                "last_name": "Maiko"
                            },
                            "is_read": True,
                            "work": {
                                "id": 7,
                                "work_code": "WK6307",
                                "writer": {
                                    "id": 1,
                                    "registration_number": "TW9801",
                                    "first_name": "Sam",
                                    "last_name": "Maiko"
                                }
                            },
                            "created_at": "2024-07-20T13:02:19.734908+03:00"
                        },
                        {
                            "id": 44,
                            "message": "work has been has been uptaken",
                            "type": "Uptaken Work",
                            "triggered_by": {
                                "id": 1,
                                "registration_number": "TW9801",
                                "first_name": "Sam",
                                "last_name": "Maiko"
                            },
                            "is_read": True,
                            "work": {
                                "id": 5,
                                "work_code": "WK7605",
                                "writer": {
                                    "id": 1,
                                    "registration_number": "TW9801",
                                    "first_name": "Sam",
                                    "last_name": "Maiko"
                                }
                            },
                            "created_at": "2024-07-20T12:59:44.330978+03:00"
                        },
                    ]
                }
            ),
            401: openapi.Response(
                description="Unauthorized",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
        },
        tags=['Notifications']
    )
    
    def get(self, request):
        notifications=request.user.notifications.all()
        # serialize 
        serializer=NotificationSerializer(notifications, many=True, context={'request':request})
        return Response(serializer.data)