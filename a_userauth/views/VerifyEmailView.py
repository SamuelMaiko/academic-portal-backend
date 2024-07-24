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
        operation_description="Receives the OTP and verifys the user's email.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'otp'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description='OTP sent to user email'),
            }
        ),
        responses={
            200: openapi.Response(
                description="OK - Email verified successfully",
                examples={
                    "application/json": {
                        "message": "OTP verification successful.",
                        "success": True
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request - Invalid OTP provided or OTP expired",
                examples={
                    "application/json": [{
                        "example1":{
                            "error":"Invalid OTP provided"
                        },
                        "example2":{
                            "error":"OTP has expired. Request for new one."
                        },
                        "example3":{
                            "error":"Email not provided"
                        },
                        "example4":{
                            "error":"OTP not provided"
                        }
                    }]
                }
            ),
            404: openapi.Response(
                description="Not Found - User with provided email not found",
                examples={
                    "application/json": {
                        "error": "User with email doesn't exist",
                        "success": False
                    }
                }
            ),
        },
        tags=['Registration']
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