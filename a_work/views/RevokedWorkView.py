from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_userauth.models import CustomUser
from a_work.serializers import DefaultWorkSerializer


class RevokedWorkView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieves the list of work that the authenticated user has had revoked.",
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
                            "id": 4,
                            "type": "RevokedUptaken",
                            "user": {
                                "id": 3,
                                "registration_number": "TW5303",
                                "first_name": "Peter",
                                "last_name": "K"
                            },
                            "work": {
                                "id": 5,
                                "work_code": "WK7605"
                            },
                            "created_at": "2024-07-19T13:12:11.347831+03:00"
                        },
                        {
                            "id": 3,
                            "type": "RevokedAssigned",
                            "user": {
                                "id": 3,
                                "registration_number": "TW5303",
                                "first_name": "Peter",
                                "last_name": "K"
                            },
                            "work": {
                                "id": 8,
                                "work_code": "WK1508"
                            },
                            "created_at": "2024-07-19T13:07:01.792041+03:00"
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
            )
        },
        tags=['Work']
    )

    def get(self, request):
        user=request.user
        work=user.default_work.filter(
            Q(type="RevokedUptaken") |
            Q(type="RevokedAssigned")
            )
        serializer=DefaultWorkSerializer(work, many=True)
        return Response(serializer.data)