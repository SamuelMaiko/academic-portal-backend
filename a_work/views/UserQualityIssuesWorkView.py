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


class UserQualityIssuesWorkView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @swagger_auto_schema(
        operation_description="Retrieve the work with quality issues associated with a specific user by ID.",
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
                description="ID of the user whose quality issues work is to be retrieved.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="List of work with quality issues associated with the user",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "type": "QualityIssues",
                            "user": {
                                "id": 3,
                                "registration_number": "TW5303",
                                "first_name": "User",
                                "last_name": "Three"
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

        work=account.default_work.filter(type="QualityIssues")
        serializer=DefaultWorkSerializer(work, many=True)
        return Response(serializer.data)