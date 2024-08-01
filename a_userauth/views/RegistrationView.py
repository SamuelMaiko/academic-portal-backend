# from userauth.HelperFunctions import SendWelcomeEmail, SendAccountActivationEmail
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from a_notifications.models import NotificationUser
from a_userauth.HelperFunctions import create_otp_model
from a_userauth.models import CustomUser, RegistrationCode
from a_userauth.serializers import UserSerializer
from a_userauth.signals import email_account_credentials, send_otp_signal


class RegistrationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes=[]
    
    @swagger_auto_schema(
        operation_description="Register a new user using a registration code and email. This endpoint creates a new account if the registration code is valid and not expired or used and emails the login credentials.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['registration_code', 'email'],
            properties={
                'registration_code': openapi.Schema(type=openapi.TYPE_STRING, description="The registration code provided for account creation."),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="The email address for the new account.")
            }
        ),
        responses={
            200: openapi.Response(
                description="Registration successful.",
                examples={
                    "application/json": {
                        "message": "Registration successful"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": "Provide registration_code, email."
                    }
                }
            ),
            404: openapi.Response(
                description="Registration code not found.",
                examples={
                    "application/json": {
                        "error": "Invalid registration code."
                    }
                }
            ),
            400: openapi.Response(
                description="Expired or already used registration code.",
                examples={
                    "application/json": {
                        "error": "Expired registration code or registration code already used."
                    }
                }
            ),
        },
        tags=['Authentication']
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
        random_password=CustomUser.objects.make_random_password()
        new_user=CustomUser.objects.create()
        new_user.set_password(random_password)
        # save the email as temporary to help in onboarding process
        new_user.temporary_email=email
        new_user.save()
        
        # associate account with the code
        reg_code_instance.user=new_user
        reg_code_instance.is_used=True
        reg_code_instance.save()
        
        
        # send the credentials to the email (reg.no and password)
        email_account_credentials.send(
            sender=None,
            registration_number=new_user.registration_number,
            password=random_password,
            email=email
            )

        # giving the user notifications
        for n in range(14,19):
            NotificationUser.objects.create(user=new_user, notification_id=n)
            
        # send a success 
        return Response({'message':"Registration successful"})