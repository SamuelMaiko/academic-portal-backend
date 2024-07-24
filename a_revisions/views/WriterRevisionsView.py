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


class WriterRevisionsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
    operation_description="Retrieve revisions for the authenticated user's submitted work.",
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
            description="List of revisions of the authenticated user's work.",
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
                    }
                ]
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
        # get the user
        user=request.user
        # get work he is the writer(assigned or uptaken)
        work_subquery=Work.objects.filter(Q(assigned_to=user) | Q(uptaken_by=user)).values_list('id',flat=True)
        # take only revisions where the writer's work is revised
        revisions=Revision.objects.filter(work_id__in=Subquery(work_subquery))
        serializer= RevisionSerializer(revisions, many=True, context={'request':request})
        return Response(serializer.data)
    