from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_userauth.models import CustomUser
from a_work.permissions import IsAdmin
from a_work.serializers import DefaultWorkSerializer


class UserRevokedWorkView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @swagger_auto_schema(
        operation_description="Retrieve the revoked work associated with a specific user by ID.",
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
                description="ID of the user whose revoked work is to be retrieved.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="List of revoked work associated with the user",
                examples={
                    "application/json": [
                        {
                            "id": 4,
                            "type": "RevokedUptaken",
                            "user": {
                                "id": 3,
                                "registration_number": "TW5303",
                                "first_name": "User",
                                "last_name": "Three"
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
                                "first_name": "User",
                                "last_name": "Three"
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
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": "Account matching query does not exist."
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
            401: openapi.Response(
                description="Unauthorized",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
        },
        tags=['Accounts']
    )


    def get(self, request, id):
        self.check_object_permissions(request, request.user)
        
        try:
            account=CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response({'error':'account matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        work=account.default_work.filter(
            Q(type="RevokedUptaken") |
            Q(type="RevokedAssigned")
            )
        serializer=DefaultWorkSerializer(work, many=True)
        return Response(serializer.data)