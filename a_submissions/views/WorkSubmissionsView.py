from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_submissions.serializers import SubmissionSerializer
from a_work.models import Work


class WorkSubmissionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieve all submissions for a specific work.",
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
                description='ID of the work whose submissions are being retrieved',
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="List of submissions for the specified work",
                examples={
                    "application/json": [
                        {
                            "id": 9,
                            "message": "Great yeah",
                            "file": "/media/submission_files/MyStudentSched_GKfbnat.pdf",
                            "sender": {
                                "id": 3,
                                "registration_number": "TW5303",
                                "first_name": "Peter",
                                "last_name": "K"
                            },
                            "work": {
                                "id": 1,
                                "work_code": "WK5201"
                            },
                            "created_at": "2024-07-24T19:08:14.636759+03:00"
                        },
                        {
                            "id": 8,
                            "message": "Hello",
                            "file": None,
                            "sender": {
                                "id": 3,
                                "registration_number": "TW5303",
                                "first_name": "Peter",
                                "last_name": "K"
                            },
                            "work": {
                                "id": 1,
                                "work_code": "WK5201"
                            },
                            "created_at": "2024-07-24T19:07:48.506239+03:00"
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
        submissions=work.submissions
        serializer=SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)