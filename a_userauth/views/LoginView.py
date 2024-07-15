from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from a_userauth.models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from a_userauth.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.conf import settings
from a_userauth.signals import send_otp_signal
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes=[]
     
    @swagger_auto_schema(
        operation_description="""Logs a user in using their email and password and returns a token. 
                        Sends an otp to email incase user account inactive.""",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['email', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Successful login",
                examples={
                    "application/json": {
                        "user": {
                            "username": "user1",
                            "email": "user1@example.com",
                            "first_name": "First",
                            "last_name": "Last"
                        },
                        "token": "abc123"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": "Provide email password."
                    }
                }
            ),
            403: openapi.Response(
                description="Forbidden",
                examples={
                    "application/json": {
                        "error": "User account is inactive. Please verify your email."
                    }
                }
            ),
            404: openapi.Response(
                description="Not found",
                examples={
                    "application/json": {
                        "error": "Invalid email or password"
                    }
                }
            ),
        },
        tags=['Authentication']
    )
    
    def post(self, request):
        email=request.data.get('email')
        password=request.data.get('password')
        
        message='Provide '
        if not email:
            message+="email "
        
        if not password:
            # message+=message=="Provide "?"":""
            message+="password."
        if message !="Provide ":
            return Response({"error":message}, status=status.HTTP_400_BAD_REQUEST)
        
        
        user=authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            # getting user token 
            token, created_token=Token.objects.get_or_create(user=user)
            user_instance=get_object_or_404(CustomUser, email=email)
            serializer=UserSerializer(user_instance)
            
            response_dict={
                "user":serializer.data,
                "token":token.key
                }
                
            return Response(response_dict, status=status.HTTP_200_OK)
        # If user returns NONE = wrong credentials
        else:
            try:
                user = CustomUser.objects.get(email=email)
                if not user.is_active:
                    send_otp_signal.send(sender=None,user=user)
                    return Response({"error": "User account is inactive. Please verify your email."}, status=status.HTTP_403_FORBIDDEN)
            except CustomUser.DoesNotExist:
                pass
            
            return Response({"error": "Invalid email or password"}, status=status.HTTP_404_NOT_FOUND)
