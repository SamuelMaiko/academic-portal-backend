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
    
    def delete(self, request, id):
        try:
            notification_association=NotificationUser.objects.get(notification_id=id, user=request.user)
        except NotificationUser.DoesNotExist:
            return Response({'error':'notification matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        notification_association.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)