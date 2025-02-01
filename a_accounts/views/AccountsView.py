from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.serializers import AccountSerializer
from a_userauth.models import CustomUser
from a_work.permissions import IsAdmin


class AccountsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @swagger_auto_schema(
        operation_description="Retrieve a list of all accounts excluding the requesting user.",
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
                description="A list of user accounts",
                examples={
                    "application/json": [
                        {
                            "id": 8,
                            "registration_number": "TW6008",
                            "first_name": "",
                            "last_name": "",
                            "email": None,
                            "is_active": True
                        },
                        {
                            "id": 7,
                            "registration_number": "TW9607",
                            "first_name": "Test",
                            "last_name": "User",
                            "email": "samuel.maiko@student.moringaschool.com",
                            "is_active": True
                        },
                    ]
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
    
    def get(self, request):
        role=request.GET.get('role', None)

        user=request.user
        # self.check_object_permissions(request, user)
        if role is not None:
            users=CustomUser.objects.filter(role=role).exclude(id=user.id).order_by('-created_at')
        else:
            users=CustomUser.objects.exclude(id=user.id).order_by('-created_at')
        serializer=AccountSerializer(users, many=True, context={"request":request})
        return Response(serializer.data)
        