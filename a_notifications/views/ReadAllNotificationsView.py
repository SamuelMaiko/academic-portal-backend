from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_notifications.models import NotificationUser
from a_notifications.serializers import NotificationSerializer


class ReadAllNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Mark all unread notifications as read for the authenticated admin user.",
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
                    "application/json": {
                        "message": "All notifications marked as read."
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
    
    def post(self, request):
        NotificationUser.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'message':'all notifications marked as read.'})