from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from a_userauth.models import CustomUser, EmailOTP
from a_userauth.serializers import ResetPasswordSerializer 
from django.contrib.auth.hashers import make_password
from a_userauth.HelperFunctions import create_otp_model
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    authentication_classes=[]
    
    @swagger_auto_schema(
        operation_description="Resets the user's password using the new password and the temporary token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'temp_token': openapi.Schema(type=openapi.TYPE_STRING, description='Temporary token sent to the user\'s email'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='New password for the user'),
            },
            required=['temp_token', 'new_password']
        ),
        responses={
            200: openapi.Response(
                description="Ok",
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
                            "example1":{
                                "error":"Invalid token."
                            },
                            "example1":{
                                "error": {
                                    "temp_token": [
                                        "This field is required."
                                    ],
                                    "new_password": [
                                        "This field is required."
                                    ],
                                    # other possible errors
                            },
                            },
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

            try:
                email_otp_instance=EmailOTP.objects.get(temp_token=temp_token)
            except EmailOTP.DoesNotExist:
                return Response({"error":"Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
            
            # setting the new password
            user=email_otp_instance.user
            user.password=make_password(new_password)
            user.save()
            
            # deleting the used temp_token along with model and creating the model again for a new temp token for next time
            user.email_otp.delete()
            create_otp_model(user)
            
            return Response({"message":"Password reset successfully", "success":True}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)