from a_userauth.HelperFunctions import generate_otp
from a_userauth.models import CustomUser, EmailOTP
from a_userauth.signals import send_otp_signal
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    authentication_classes=[]
    
    @swagger_auto_schema(
        operation_description="""Initiates a password reset process by sending an OTP to the user's email.
                                The OTP can be used to reset the password. If the email is not associated with
                                any user, an appropriate error message is returned.""",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='The email address of the user who wants to reset their password.')
            },
            required=['email']
        ),
        responses={
            200: openapi.Response(
                description="OTP sent successfully",
                examples={
                    "application/json": {
                        "message": "OTP sent to email"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": "Provide email."
                    }
                }
            ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "message": "User with email does not exist."
                    }
                }
            )
        },
        tags=['Forgot Password']
    )


    def post(self, request):
        email=request.data.get("email")
        if not email:
            return Response({'error':'Provide email.'})
        try:
            user=CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'message':"User with email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # generating new otp (because we use the same for email verification earlier)
        new_otp=generate_otp()
        # updating the otp
        EmailOTP.objects.filter(user=user).update(otp=new_otp, timestamp=timezone.now())
        # signal to send otp to user's email
        send_otp_signal.send(
            sender=None,
            user=user,
            type="first_time_request"
            )
        
        return Response({'message':"OTP sent to email"})
        
        