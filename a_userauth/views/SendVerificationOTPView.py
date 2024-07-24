from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_userauth.HelperFunctions import generate_otp
from a_userauth.models import CustomUser, EmailOTP
from a_userauth.signals import send_verification_otp


class SendVerificationOTPView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Sends a new OTP to the user's email for verification. ",
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
                description="Successful OTP sending",
                examples={
                    "application/json": {
                        "message": "OTP sent successfully"
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
            )
        },
        tags=['Email Verification']
    )
    
    def post(self, request):
        user=request.user
        new_otp=generate_otp()
        # updating the otp
        EmailOTP.objects.filter(user=user).update(otp=new_otp, timestamp=timezone.now())
        send_verification_otp.send(sender=None, user=user)
        
        return Response({'message':'Otp sent successfully'})

        