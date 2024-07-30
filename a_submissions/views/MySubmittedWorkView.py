from django.db.models import Subquery
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_submissions.models import Submission
from a_submissions.serializers import SubmittedWorkSerializer
from a_work.models import Work


class MySubmittedWorkView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieve the submitted work for the authenticated user.",
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
                description="List of submitted works.",
                examples={
                    "application/json": [
                        {
                            "id": 8,
                            "work_code": "WK1508",
                            "words": 2000,
                            "submission": {
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
                            }
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
        tags=['Profile']
    )
    
    def get(self, request):
        user=request.user        
        sub_work=Submission.objects.filter(sender=user).order_by("-created_at").values("work_id").distinct().values_list("work_id", flat=True)
        
        submitted_work=Work.objects.filter(id__in=sub_work)
        serializer=SubmittedWorkSerializer(submitted_work, many=True, context={'user':user})
        return Response(serializer.data)