from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_notifications.models import Notification
from a_revisions.models import Revision
from a_revisions.serializers import RevisionMessageSerializer
from a_work.models import Work


class SendRevisionMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request,id):
        try:
            revision = Revision.objects.get(pk=id)
        except Revision.DoesNotExist:
            return Response({'error': 'Revision matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        data=request.data.copy()
        data['sender']=request.user
        data["revision"]=revision.id

        serializer=RevisionMessageSerializer(data=data, context={'request':request})
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)