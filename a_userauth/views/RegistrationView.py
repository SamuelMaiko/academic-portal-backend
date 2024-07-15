from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from a_userauth.models import CustomUser, RegistrationCode
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from a_userauth.serializers import UserSerializer
# from userauth.HelperFunctions import SendWelcomeEmail, SendAccountActivationEmail
from a_userauth.HelperFunctions import create_otp_model
from a_userauth.signals import send_otp_signal, email_account_credentials
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
        # take reg code, email, 
        registration_code=request.data.get("registration_code")
        email=request.data.get("email")

        message='Provide '
        if not registration_code:
            message+="registration_code "
        
        if not email:
            message+=", email."
            
        if message !="Provide ":
            return Response({"error":message}, status=status.HTTP_400_BAD_REQUEST)
        # check if reg code has expired(8hrs) or used
        try:
            reg_code_instance=RegistrationCode.objects.get(code=registration_code)
        except RegistrationCode.DoesNotExist:
            return Response({'error':'Invalid registration code.'}, status=status.HTTP_404_NOT_FOUND)
        
        if reg_code_instance.is_expired:
            return Response({'error':'Expired registration code.'}, status=status.HTTP_400_BAD_REQUEST)

        if reg_code_instance.is_used:
            return Response({'error':'registration code already used.'}, status=status.HTTP_400_BAD_REQUEST)
            
        # if not create an account
        new_user=CustomUser.objects.create()
        new_user.set_password("1234")
        new_user.save()
        
        # associate account with the code
        reg_code_instance.user=new_user
        reg_code_instance.is_used=True
        reg_code_instance.save()
        # send the credentials to the email (reg.no and password)
        email_account_credentials.send(
            sender=None,
            registration_number=new_user.registration_number,
            password="1234",
            email=email
            )
        # send a success 
        return Response({'message':"Registration successful"})