from django.contrib.auth.hashers import make_password
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from a_userauth.HelperFunctions import create_otp_model
from a_userauth.models import CustomUser, EmailOTP
from a_userauth.serializers import ResetPasswordSerializer


class SubmitNewPasswordView(APIView):
    permission_classes = [AllowAny]
    authentication_classes=[]
    
    @swagger_auto_schema(
        operation_description="Submits a new password using a temporary token. Allows users to set a new password after verifying the OTP.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'temp_token': openapi.Schema(type=openapi.TYPE_STRING, description='Temporary token received during OTP verification'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='New password to be set for the user'),
            },
            required=['temp_token', 'new_password']
        ),
        responses={
            200: openapi.Response(
                description="Password reset successfully.",
                examples={
                    "application/json": {
                        "message": "Password reset successfully",
                        "success": True
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": [
                        {
                            "example1": {
                                "error": "temp_token not provided"
                            },
                            "example2": {
                                "error": "new_password not provided"
                            },
                            "example3": {
                                "error": "Invalid token."
                            }
                        }
                    ]
                }
            ),
        },
        tags=['Forgot Password']
    )
     
    def post(self, request):
        serializer=ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            temp_token=serializer.validated_data["temp_token"]
            new_password=serializer.validated_data["new_password"]

            if not temp_token:
                return Response({'error':'temp_token not provided'}, status=status.HTTP_400_BAD_REQUEST)

            if not new_password:
                return Response({'error':'new_password not provided'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                email_otp_instance=EmailOTP.objects.get(temp_token=temp_token)
            except EmailOTP.DoesNotExist:
                return Response({"error":"Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
            
            # setting the new password
            user=email_otp_instance.user
            user.password=make_password(new_password)
            user.save()
            
            # deletinng (refreshing) temp_token to prevent being reused again 
            user.otp.delete()
            create_otp_model(user)
            
            return Response({"message":"Password reset successfully", "success":True}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)