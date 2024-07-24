from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_work.serializers import AssignedUptakenSerializer


class UptakenWorkView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieves the list of work that the authenticated user has uptaken.",
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
                            "id": 12,
                            "work_code": "WK16012",
                            "deadline": "2024-07-17T15:00:00+03:00",
                            "words": 1500,
                            "type": "Essay",
                            "status": "Not started",
                            "is_submitted": False,
                            "uptaken_is_read": False,
                            "assigned_is_read": False
                        },
                        {
                            "id": 13,
                            "work_code": "WK160164",
                            "deadline": "2024-07-17T15:00:00+03:00",
                            "words": 2000,
                            "type": "Reflection Paper",
                            "status": "Not started",
                            "is_submitted": False,
                            "uptaken_is_read": False,
                            "assigned_is_read": False
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
        work=request.user.uptaken_work
        serializer=AssignedUptakenSerializer(work, many=True)
        return Response(serializer.data)