from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_notifications.models import Notification
from a_work.models import Work


class UptakeWorkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            work=Work.objects.get(pk=id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        if work.has_writer:
            return Response({'error':'Work has already been allocated.'}, status=status.HTTP_400_BAD_REQUEST)

        work.uptaken_by=request.user
        work.save()
        # adding a notification
        notification=Notification.objects.create(
            type="Uptaken Work",
            message="work has been has been uptaken",
            triggered_by=request.user,
            work=work
            )
        admins=get_admins()
        notification.users.add(*admins)

        return Response({'message':'Work has been uptaken successfully.'})
        
        