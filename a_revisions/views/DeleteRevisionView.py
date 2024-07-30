from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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
    
    @swagger_auto_schema(
        operation_description="Delete a specific revision by ID.",
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
                description="ID of the revision to delete.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            204: openapi.Response(
                description="Revision successfully deleted."
            ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": "Revision matching query does not exist."
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

    def delete(self, request,id):
        self.check_object_permissions(request, request.user)
        try:
            revision= Revision.objects.get(pk=id)
        except Revision.DoesNotExist:
            return Response({'error':'revision matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        revision.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)