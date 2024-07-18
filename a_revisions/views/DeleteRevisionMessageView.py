from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_revisions.models import RevisionMessage
from a_revisions.permissions import IsRevisionMessageSender


class DeleteRevisionMessageView(APIView):
    permission_classes = [IsAuthenticated, IsRevisionMessageSender]

    def delete(self, request, id):      
        try:
            revision_message=RevisionMessage.objects.get(pk=id)
        except RevisionMessage.DoesNotExist:
            return Response({'error':'revision message matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, revision_message)
        revision_message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)