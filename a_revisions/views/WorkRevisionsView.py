from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_revisions.serializers import RevisionSerializer
from a_work.models import Work


class WorkRevisionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieve all revisions for a specific work.",
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Bearer token for authentication',
                required=True
            ),
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='ID of the work whose revisions are being retrieved',
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Retrieves all revisions for the specified work.",
                examples={
                    "application/json": [
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
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": "Work matching query does not exist."
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
        tags=['Work']
    )

    def get(self, request, id):
        try:
            work= Work.objects.get(pk=id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        revisions=work.revisions
        serializer=RevisionSerializer(revisions, many=True, context={'request':request})
        return Response(serializer.data)