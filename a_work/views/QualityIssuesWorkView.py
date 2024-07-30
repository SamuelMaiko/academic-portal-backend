from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_userauth.models import CustomUser
from a_work.serializers import DefaultWorkSerializer


class QualityIssuesWorkView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieves the list of work that the user did and has quality issues.",
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Bearer token for authentication',
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Success",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "type": "QualityIssues",
                            "user": {
                                "id": 3,
                                "registration_number": "TW5303",
                                "first_name": "Peter",
                                "last_name": "K"
                            },
                            "work": {
                                "id": 4,
                                "work_code": "WK2304"
                            },
                            "created_at": "2024-07-19T08:20:07.883323+03:00"
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
        tags=['Work']
    )

    def get(self, request):
        user=request.user
        work=user.default_work.filter(type="QualityIssues")
        serializer=DefaultWorkSerializer(work, many=True)
        return Response(serializer.data)