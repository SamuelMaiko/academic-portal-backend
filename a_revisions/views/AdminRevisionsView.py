from django.db.models import Q, Subquery
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
from a_revisions.serializers import RevisionSerializer
from a_work.models import Work
from a_work.permissions import IsAdmin


class AdminRevisionsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @swagger_auto_schema(
    operation_description="Retrieve revisions where the authenticated admin is the reviewer.",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer token",
            type=openapi.TYPE_STRING,
            required=True
        ),
    ],
    responses={
        200: openapi.Response(
            description="List of revisions where the authenticated admin is the reviewer.",
            examples={
                "application/json": [
                    {
                        "id": 3,
                        "submit_before": "2024-08-01T17:30:00+03:00",
                        "work": {
                            "id": 12,
                            "work_code": "WK16012"
                        },
                        "status": "Not started",
                        "reviewer": {
                            "id": 1,
                            "registration_number": "TW9801",
                            "first_name": "Sam",
                            "last_name": "Maiko"
                        },
                        "is_read": True,
                        "created_at": "2024-07-19T17:56:15.614392+03:00"
                    },
                    {
                        "id": 2,
                        "submit_before": "2024-08-01T17:30:00+03:00",
                        "work": {
                            "id": 8,
                            "work_code": "WK1508"
                        },
                        "status": "Not started",
                        "reviewer": {
                            "id": 1,
                            "registration_number": "TW9801",
                            "first_name": "Sam",
                            "last_name": "Maiko"
                        },
                        "is_read": False,
                        "created_at": "2024-07-17T15:29:07.207329+03:00"
                    }
                ]
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
        401: openapi.Response(
            description="Unauthorized",
            examples={
                "application/json": {
                    "detail": "Authentication credentials were not provided."
                }
            }
        )
    },
    tags=['Revisions']
)

    def get(self, request):
        user=request.user
        # check if admin
        self.check_object_permissions(request, user)
        # get revision where user is reviewer
        revisions=Revision.objects.filter(reviewer=user)
        # serialize
        serializer= RevisionSerializer(revisions, many=True, context={'request':request})
        return Response(serializer.data)