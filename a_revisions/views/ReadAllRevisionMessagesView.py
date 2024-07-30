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
from a_work.models import Work


class ReadAllRevisionMessagesView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Mark all revision messages as read for a specific revision by ID. NOTE: It marks the other user's mages as read.",
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
                description="ID of the revision whose messages are to be marked as read.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="All messages marked as read.",
                examples={
                    "application/json": {
                        "message": "All messages marked as read"
                    }
                }
            ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": "revision matching query does not exist."
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
        },
        tags=['Revisions']
    )

    def post(self, request,id):
        try:
            revision= Revision.objects.get(pk=id)
        except Revision.DoesNotExist:
            return Response({'error':'revision matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
        # mark the other user's messages as read
        revision.messages.exclude(sender=request.user).update(is_read=True)
        return Response({'message':'All messages marked as read'})