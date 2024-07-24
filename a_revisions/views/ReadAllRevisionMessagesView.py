from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_notifications.models import Notification
from a_revisions.models import Revision
from a_work.models import Work


class ReadAllRevisionMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request,id):
        try:
            revision= Revision.objects.get(pk=id)
        except Revision.DoesNotExist:
            return Response({'error':'revision matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
        # mark the other user's messages as read
        revision.messages.exclude(sender=request.user).update(is_read=True)
        return Response({'message':'All messages marked as read'})