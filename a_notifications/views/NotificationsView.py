from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_notifications.serializers import NotificationSerializer
from a_work.permissions import IsAdmin


class NotificationsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        notifications=request.user.notifications.all()
        # serialize 
        serializer=NotificationSerializer(notifications, many=True, context={'request':request})
        return Response(serializer.data)