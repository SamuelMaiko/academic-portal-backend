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
from a_revisions.serializers import EditRevisionSerializer
from a_work.models import Work
from a_work.permissions import IsAdmin


class EditRevisionView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @swagger_auto_schema(
        operation_description="Edit the 'submit_before' field of a specific revision by ID.",
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
                description="ID of the revision to edit.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'submit_before': openapi.Schema(type=openapi.TYPE_STRING, description='Submission deadline')
            },
            required=['submit_before']
        ),
        responses={
            200: openapi.Response(
                description="Revision successfully edited.",
                examples={
                    "application/json": {
                        "id": 1,
                        "submit_before": "2024-07-25T12:00:00Z"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "submit_before": ["This field is required."]
                    }
                }
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


    def put(self, request,id):
        self.check_object_permissions(request, request.user)

        try:
            revision= Revision.objects.get(pk=id)
        except Revision.DoesNotExist:
            return Response({'error':'revision matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # still using the same serializer for editing
        serializer=EditRevisionSerializer(revision, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        