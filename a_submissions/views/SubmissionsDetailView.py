from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_submissions.models import Submission
from a_submissions.serializers import SubmissionSerializer


class SubmissionsDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve the details of a submission by ID.",
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
                description="ID of the submission to retrieve details for.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="OK.",
                examples={
                    "application/json": [
                            {
                                "id": 6,
                                "message": "Forgot,latest one.",
                                "file": "/media/submission_files/MyStudentSched.pdf",
                                "file_download_link": "http://localhost:8000/api/work/download/1/",
                                "sender": {
                                    "id": 3,
                                    "registration_number": "TW5303",
                                    "first_name": "Peter",
                                    "last_name": "K"
                                },
                                "work": {
                                    "id": 4,
                                    "work_code": "WK2304"
                                },
                                "created_at": "2024-07-19T12:48:58.646425+03:00"
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
            ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": "submission matching query does not exist."
                    }
                }
            ),
        },
        tags=['Submissions']
    )
    
    def get(self, request, id):      
        try:
            submission=Submission.objects.get(pk=id)
        except Submission.DoesNotExist:
            return Response({'error':'submission matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        serializer=SubmissionSerializer(submission, context={"request":request})
        return Response(serializer.data)