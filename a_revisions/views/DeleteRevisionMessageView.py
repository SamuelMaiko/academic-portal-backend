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
    
    @swagger_auto_schema(
        operation_description="Delete a specific revision message by ID.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the revision message to be deleted.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            204: openapi.Response(
                description="No Content, revision message deleted successfully."
            ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": "revision message matching query does not exist."
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
            ),
            403: openapi.Response(
                description="Permission Denied",
                examples={
                    "application/json": {
                        "detail": "You do not have permission to perform this action."
                    }
                }
            ),
        },
        tags=['Revisions']
    )

    def delete(self, request, id):      
        try:
            revision_message=RevisionMessage.objects.get(pk=id)
        except RevisionMessage.DoesNotExist:
            return Response({'error':'revision message matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, revision_message)
        revision_message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)