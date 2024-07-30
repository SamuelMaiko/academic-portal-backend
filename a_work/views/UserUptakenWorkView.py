from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_userauth.models import CustomUser
from a_work.permissions import IsAdmin
from a_work.serializers import AssignedUptakenSerializer


class UserUptakenWorkView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @swagger_auto_schema(
        operation_description="Retrieve the work uptaken by a specific user by ID.",
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
                description="ID of the user whose uptaken work is to be retrieved.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="List of work assigned to the user",
                examples={
                    "application/json": [
                        {
                            "id": 13,
                            "work_code": "WK13013",
                            "deadline": "2024-07-17T15:00:00+03:00",
                            "words": 1500,
                            "type": "Essay",
                            "status": "Not started",
                            "is_submitted": False,
                            "uptaken_is_read": False,
                            "assigned_is_read": False
                        },
                        {
                            "id": 7,
                            "work_code": "WK6307",
                            "deadline": "2024-07-17T15:00:00+03:00",
                            "words": 1500,
                            "type": "Reflection Paper",
                            "status": "Not started",
                            "is_submitted": False,
                            "uptaken_is_read": False,
                            "assigned_is_read": False
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
        work=account.uptaken_work
        serializer=AssignedUptakenSerializer(work, many=True)
        return Response(serializer.data)