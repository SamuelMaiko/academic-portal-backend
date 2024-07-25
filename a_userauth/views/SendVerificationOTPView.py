from a_userauth.HelperFunctions import generate_otp
from a_userauth.models import CustomUser, EmailOTP
from a_userauth.signals import send_verification_otp
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class SendVerificationOTPView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Sends a new OTP to the user's email for verification (updates the user's email). ",
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
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email of the user to send OTP.'),
            },
            required=['email']
        ),
        responses={
            200: openapi.Response(
                description="Successful OTP sending",
                examples={
                    "application/json": {
                        "message": "OTP sent successfully"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        'error':"Provide email"
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
            ),
        },
        tags=['Email Verification']
    )
    
    def post(self, request):
        user=request.user
        email=request.data.get("email")
        
        if not email:
            return Response({'error':"Provide email"}, status=status.HTTP_400_BAD_REQUEST)

        new_otp=generate_otp()
        # updating the otp
        EmailOTP.objects.filter(user=user).update(otp=new_otp, timestamp=timezone.now())

        # updating user's email
        try:
            user.email=email
            user.save()
        except:
            return Response({'error':"User with email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        send_verification_otp.send(sender=None, user=user, email=email)
        
        return Response({'message':'Otp sent successfully'})

        