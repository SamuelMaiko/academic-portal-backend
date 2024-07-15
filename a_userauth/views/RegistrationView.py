from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from a_userauth.models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from a_userauth.serializers import UserSerializer
# from userauth.HelperFunctions import SendWelcomeEmail, SendAccountActivationEmail
from a_userauth.HelperFunctions import create_otp_model
from a_userauth.signals import send_otp_signal
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




class RegistrationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes=[]
    
    @swagger_auto_schema(
        operation_description="Register a new user and sends an OTP to verify the email.",
        request_body=UserSerializer,  # Use your UserSerializer here
        responses={
            201: openapi.Response(
                description="Created - Registration successful",
                examples={
                    "application/json": {
                        "message": "Registration successful, OTP sent.",
                        "success": True
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request - Invalid data provided or user with same email exists",
                examples={
                    "application/json": {
                        "error": "A user with the same email exists",
                        "success": False
                    }
                }
            ),
        },
        tags=['Registration']
    )

    def post(self, request):
        email=request.data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            return Response({"error":"A user with same email exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            data=serializer.validated_data
            data['is_active']=False
            user=serializer.save()

            # create OTP model for user
            create_otp_model(user)
            # sending otp
            send_otp_signal.send(sender=None,user=user)
            
            return Response({"message":"registration successful, OTP sent.", "success":True}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors,"success":False}, status=status.HTTP_400_BAD_REQUEST)
