from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_userauth.models import CustomUser, EmailOTP


class VerifyEmailView(APIView):    
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Verifies the email of the user by validating the OTP sent to their email.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description='OTP sent to the user\'s email'),
            },
            required=['otp']
        ),
        responses={
            200: openapi.Response(
                description="Successful OTP verification",
                examples={
                    "application/json": {
                        "message": "OTP verification successful.",
                        "success": True
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": [
                        {
                            "error": "OTP not provided",
                            "error": "OTP has expired. Request for new one.",
                            "error": "Invalid OTP provided"
                        }
                    ]
                }
            )
        },
        tags=['Email Verification']
    )
    
    def post(self, request):
        user_entered_otp=request.data.get("otp")
        user=request.user
        
        if not user_entered_otp:
            return Response({"error":"OTP not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        email_otp=EmailOTP.objects.get(user=user)
        
        # if otp matches 
        if email_otp.otp==user_entered_otp:
            # if otp not expired
            if not email_otp.is_expired:
                user.is_verified=True
                user.save()
                
                return Response({"message":"OTP verification successful.","success":True})
            # if otp  not expired
            else:
                return Response({"error":"OTP has expired. Request for new one."}, status=status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response({"error":"Invalid OTP provided"}, status=status.HTTP_400_BAD_REQUEST)