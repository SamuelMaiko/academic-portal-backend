from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_userauth.HelperFunctions import generate_otp
from a_userauth.models import CustomUser, EmailOTP
from a_userauth.signals import send_otp_signal


class DeactivateAccountView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Deactivates the authenticated user's account.",
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                description='Bearer token for authentication',
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Account successfully deactivated",
                examples={
                    "application/json": {
                        "message": "Account deactivated successfully"
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized",
                examples={
                    "application/json": {
                        "error": "Authentication credentials were not provided."
                    }
                }
            ),
        },
        tags=['Account Management']
    )
    
    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()

        return Response({'message': 'Account deactivated successfully'})