from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_revisions.models import RevisionMessage
from a_revisions.permissions import IsRevisionMessageSender
from a_revisions.serializers import RevisionMessageSerializer


class EditRevisionMessageView(APIView):
    permission_classes = [IsAuthenticated, IsRevisionMessageSender]

    def put(self, request, id):      
        try:
            revision_message=RevisionMessage.objects.get(pk=id)
        except RevisionMessage.DoesNotExist:
            return Response({'error':'revision message matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        # checking permissions
        self.check_object_permissions(request, revision_message)

        data=request.data.copy()
        data["revision"]=revision_message.revision.id
        data["sender"]=revision_message.sender.id
        serializer=RevisionMessageSerializer(revision_message,data=data, context={'request':request})
        if serializer.is_valid():
            serializer.save(sender=revision_message.sender)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)