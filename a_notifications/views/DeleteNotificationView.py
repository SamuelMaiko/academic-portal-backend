from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_notifications.models import NotificationUser
from a_notifications.serializers import NotificationSerializer


class DeleteNotificationView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Delete a specific notification for the authenticated user.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True
            ),
             openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the notification to be deleted.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            204: openapi.Response(
                description="No Content",
                examples={
                    "application/json": {}
                }
            ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": "Notification matching query does not exist."
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            )
        },
        tags=['Notifications']
    )
    
    def delete(self, request, id):
        try:
            notification_association=NotificationUser.objects.get(notification_id=id, user=request.user)
        except NotificationUser.DoesNotExist:
            return Response({'error':'notification matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        notification_association.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)