from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_submissions.models import Submission
from a_submissions.serializers import AllSubmissionsSerializer
from a_work.models import Work
from a_work.permissions import IsAdmin


class AllSubmissionsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="List of all submissions made by all users accessible by only admins.",
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
                description="List of all submissions made by all users.",
                examples={
                    "application/json": [
                            {
                                "id": 6,
                                "message": "Forgot,latest one.",
                                "file": "http://localhost:8000/media/submission_files/MyStudentSched.pdf",
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
                                "created_at": "2024-07-19T12:48:58.646425+03:00",
                                "is_claimed": False,
                                "claimed_by": {
                                    "id": None,
                                    "registration_number": "",
                                    "first_name": "No one",
                                    "last_name": "at all."
                                },
                                "claimed_by_me": False
                            },
                            {
                                "id": 5,
                                "message": "Here is the work",
                                "file": "http://localhost:8000/media/submission_files/smiling-man.jpg",
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
                                "created_at": "2024-07-19T08:19:25.551731+03:00",
                                "is_claimed": False,
                                "claimed_by": {
                                    "id": None,
                                    "registration_number": "",
                                    "first_name": "No one",
                                    "last_name": "at all."
                                },
                                "claimed_by_me": False
                            },
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
            403: openapi.Response(
                description="Permission Denied",
                examples={
                    "application/json": {
                        "detail": "You do not have permission to perform this action."
                    }
                }
            ),
        },
        tags=['Submissions']
    )
    
    def get(self, request):
        self.check_object_permissions(request, request.user)

        submissions=Submission.objects.all()
        serializer=AllSubmissionsSerializer(submissions, many=True, context={'request':request})
        return Response(serializer.data)