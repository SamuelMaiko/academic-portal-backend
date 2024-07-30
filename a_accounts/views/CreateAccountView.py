from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.serializers import CreateAccountSerializer
from a_userauth.models import CustomUser
from a_work.permissions import IsAdmin


class CreateAccountView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @swagger_auto_schema(
        operation_description="Create a new account.",
        request_body=CreateAccountSerializer,
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
            201: openapi.Response(
                description="Account created successfully",
                examples={
                    "application/json": {
                        "id": 1,
                        "registration_number": "123456",
                        "first_name": "John",
                        "last_name": "Doe",
                        "email": "john.doe@example.com",
                        "is_active": True
                    }
                    
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "registration_number": ["This field is required."],
                        "email": ["Enter a valid email address."]
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
    
    def post(self, request):
        user=request.user
        self.check_object_permissions(request, user)

        serializer=CreateAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        