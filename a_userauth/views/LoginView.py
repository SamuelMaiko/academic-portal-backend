from a_userauth.models import CustomUser
from a_userauth.serializers import UserSerializer
from a_userauth.signals import send_otp_signal
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes=[]
    
    @swagger_auto_schema(
        operation_description="""Logs a user in using their registration number and password and returns a token.
                                If the credentials are correct, it also returns user details and JWT tokens. 
                                Otherwise, it returns an error message.""",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'registration_number': openapi.Schema(type=openapi.TYPE_STRING, description='The registration number of the user.'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='The password of the user.')
            },
            required=['registration_number', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Successful login",
                examples={
                    "application/json": {
                        "user": {
                            "registration_number": "TW5303",
                            "email": "peterkenyatta631@gmail.com",
                            "profile_picture_absolute": "http//:localhost:8000/media/profile_pics/Screenshot_2024-06-24_183856.png",        
                            "first_name": "Peter",
                            "last_name": "Josh",
                            "details_filled": True,
                            "profile_completed": False,
                            "password_changed": False,
                            "is_verified":False
                        },
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMjQzMTcxMiwiaWF0IjoxNzIxODI2OTEyLCJqdGkiOiIyODM1ZGVmMWU1Nzg0MTNmYTBmYjdhOTc2NGUxOWFjZSIsInVzZXJfaWQiOjN9.6268BEgjgGrTTL0aUk3PKrudOnT6WE1HDyRXMB1jHcw",
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxODQ1ODEyLCJpYXQiOjE3MjE4MjY5MTIsImp0aSI6IjBhMDA1YzEzY2EzMTQyMzFhZTA0NjcxNGU0NDBjYzBiIiwidXNlcl9pZCI6M30.BdQfpLMqU2VZWYvr3DbJT35MCMf8DpAtLEVUSLgAxuk"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": "Provide registration_number, password."
                    }
                }
            ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": "Invalid registration number or password"
                    }
                }
            )
        },
        tags=['Authentication']
    )    
    
    def post(self, request):
        registration_number=request.data.get('registration_number')
        password=request.data.get('password')
        
        message='Provide '
        if not registration_number:
            message+="registration_number "
        
        if not password:
            message+=", password."
            
        if message !="Provide ":
            return Response({"error":message}, status=status.HTTP_400_BAD_REQUEST)
            # activating if inactive
        usr=CustomUser.objects.filter(registration_number=registration_number).first()
        if usr and not usr.is_active:
            usr.is_active=True
            usr.save()


        
        
        user=authenticate(request, username=registration_number, password=password)
        
        if user is not None:
            login(request, user)
            # getting user token 
            user_instance=get_object_or_404(CustomUser, registration_number=registration_number)
            serializer=UserSerializer(user_instance, context={'request':request})
            
            response=serializer.data.copy()
            response["temporary_email"]=user.temporary_email
            response["details_filled"]=user.onboarding.details_filled
            response["profile_completed"]=user.onboarding.profile_completed
            response["password_changed"]=user.onboarding.password_changed
            response["is_verified"]=user.is_verified
            response["dark_mode"]=user.preferences.dark_mode
            
            # jwt
            refresh = RefreshToken.for_user(user)

            response_dict={
                "user":response,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                }
                
            return Response(response_dict, status=status.HTTP_200_OK)
        # If user returns NONE = wrong credentials
        else:
            return Response({"error": "Invalid registration number or password"}, status=status.HTTP_404_NOT_FOUND)
