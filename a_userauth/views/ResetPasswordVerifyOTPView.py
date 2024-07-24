from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from a_userauth.models import CustomUser, EmailOTP


class ResetPasswordVerifyOTPView(APIView):
    permission_classes = [AllowAny]
    authentication_classes=[]
    
    @swagger_auto_schema(
        operation_description="""Verifies the OTP sent to email for resetting the password.
        NOTE: the temp_token returned is used when submitting new password.
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email of the user'),
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description='OTP sent to the user\'s email'),
            },
            required=['email', 'otp']
        ),
        responses={
            200: openapi.Response(
                description="OTP verification successful.",
                examples={
                    "application/json": {
                        "temp_token": "temporary_token",
                        "message": "OTP verification successful.",
                        "success": True
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": {
                        "error": "Email not provided",
                        "error": "OTP not provided",
                        "error": "Invalid OTP provided",
                        "error": "OTP has expired. Request for new one."
                    }
                }
            ),
            404: openapi.Response(
                description="Not found",
                examples={
                    "application/json": {
                        "error": "User with email doesn't exist"
                    }
                }
            ),
        },
        tags=['Forgot Password']
    )
    
    def post(self, request):
        email=request.data.get("email")
        user_entered_otp=request.data.get("otp")
        
        if not email:
            return Response({"error":"Email not provided"}, status=status.HTTP_400_BAD_REQUEST)
        if not user_entered_otp:
            return Response({"error":"OTP not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        user=CustomUser.objects.filter(email=email).first()
        
        if not user:
            return Response({"error":"user with email doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        email_otp=EmailOTP.objects.get(user=user)
        
        # if otp matches 
        if email_otp.otp==user_entered_otp:
            # if otp not expired
            if not email_otp.is_expired:
                # retrieving temporary token 
                temp_token=email_otp.temp_token
                
                return Response({"temp_token":str(temp_token),"message":"OTP verification successful.","success":True}, status=status.HTTP_200_OK)
            # if otp  not expired
            else:
                return Response({"error":"OTP has expired. Request for new one."}, status=status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response({"error":"Invalid OTP provided"}, status=status.HTTP_400_BAD_REQUEST)