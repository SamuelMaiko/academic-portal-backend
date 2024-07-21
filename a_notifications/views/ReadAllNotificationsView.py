from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_notifications.models import NotificationUser
from a_notifications.serializers import NotificationSerializer
from a_work.permissions import IsAdmin


class ReadAllNotificationsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def post(self, request):
        NotificationUser.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'message':'all notifications marked as read.'})