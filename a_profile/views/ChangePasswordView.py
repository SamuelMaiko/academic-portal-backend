from django.contrib.auth.hashers import check_password
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_profile.serializers import ChangePasswordSerializer
from a_userauth.models import CustomUser


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
    operation_description="Change the password for the authenticated user.",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer token",
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'type',
            openapi.IN_QUERY,
            description="Type of password change operation i.e. use (type=first) while on onboarding page else use the plain endpoint i.e no param .",
            type=openapi.TYPE_STRING,
            required=False
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'old_password': openapi.Schema(type=openapi.TYPE_STRING, description='Current password of the user.'),
            'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='New password for the user.')
        },
        required=['old_password', 'new_password']
    ),
    responses={
        200: openapi.Response(
            description="Password changed successfully.",
            examples={
                "application/json": {
                    "message": "Password changed successfully."
                }
            }
        ),
        400: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    "old_password": ["Wrong password."],
                    "new_password": ["New password cannot be the same as the old password."]
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
        )
    },
    tags=['Profile']
)
    
    def put(self, request):
        search_param=request.GET.get('type','')

        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            # Check if the old password is correct
            if not check_password(old_password, user.password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if the new password is the same as the old password
            if old_password == new_password:
                return Response({"new_password": ["New password cannot be the same as the old password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # Set the new password
            user.set_password(new_password)
            user.save()

            if search_param=="first":
                user.onboarding.password_changed=True
                user.onboarding.save()

            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            