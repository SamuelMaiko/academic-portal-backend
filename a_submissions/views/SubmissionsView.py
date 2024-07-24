from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_submissions.models import Submission
from a_submissions.serializers import SubmissionSerializer
from a_work.models import Work


class SubmissionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieve the submissions made by the authenticated user.",
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
                description="List of submissions made by the user.",
                examples={
                    "application/json": [
                            {
                                "id": 4,
                                "message": "Her is my first submission sir",
                                "file": "/media/submission_files/Remaining_UI_D8m4sQL.docx",
                                "sender": {
                                    "id": 1,
                                    "registration_number": "TW9801",
                                    "first_name": "Sam",
                                    "last_name": "Maiko"
                                },
                                "work": {
                                    "id": 8,
                                    "work_code": "WK1508"
                                },
                                "created_at": "2024-07-17T14:50:05.414144+03:00"
                            },
                            {
                                "id": 3,
                                "message": "Her is my first submission sir",
                                "file": "/media/submission_files/Remaining_UI_8OrMemO.docx",
                                "sender": {
                                    "id": 1,
                                    "registration_number": "TW9801",
                                    "first_name": "Sam",
                                    "last_name": "Maiko"
                                },
                                "work": {
                                    "id": 8,
                                    "work_code": "WK1508"
                                },
                                "created_at": "2024-07-17T13:15:03.668814+03:00"
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
        },
        tags=['Submissions']
    )
    
    def get(self, request):
        user=request.user        
        submissions=Submission.objects.filter(sender=user)
        serializer=SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)