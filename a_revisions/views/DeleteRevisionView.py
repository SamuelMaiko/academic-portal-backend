from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_notifications.models import Notification
from a_revisions.models import Revision
from a_revisions.serializers import CreateRevisionSerializer
from a_work.models import Work
from a_work.permissions import IsAdmin


class DeleteRevisionView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request,id):
        self.check_object_permissions(request, request.user)
        try:
            revision= Revision.objects.get(pk=id)
        except Revision.DoesNotExist:
            return Response({'error':'revision matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        revision.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)