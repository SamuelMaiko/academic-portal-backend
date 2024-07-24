from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from a_userauth.HelperFunctions import generate_otp
from a_userauth.models import CustomUser, EmailOTP
from a_userauth.signals import send_otp_signal


class NewOtpGenerationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes=[]
    
    @swagger_auto_schema(
        operation_description="Generates and sends a new OTP to the user's email for password reset.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email of the user requesting a new OTP'),
            },
            required=['email']
        ),
        responses={
            200: openapi.Response(
                description="New OTP generated and sent successfully.",
                examples={
                    "application/json": {
                        "message": "OTP sent to email",
                        "success": True
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": {
                        "error": "Email not provided"
                    }
                }
            ),
            404: openapi.Response(
                description="Not found",
                examples={
                    "application/json": {
                        "error": "User with email does not exist"
                    }
                }
            ),
        },
        tags=['Forgot Password']
    )

        
    def post(self, request):
        email=request.data.get("email")
        
        if not email:
            return Response({"error":"Email not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user=CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error':"User with email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        # generating new otp
        new_otp=generate_otp()
        # updating user's otp
        EmailOTP.objects.filter(user=user).update(otp=new_otp, timestamp=timezone.now())
        
        send_otp_signal.send(sender=None,user=user, type="new_otp_request")
        
        return Response({"message":"OTP sent to email", "success":True }, status=status.HTTP_200_OK)
        