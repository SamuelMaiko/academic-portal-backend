from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from a_userauth.models import EmailOTP
from a_userauth.HelperFunctions import generate_otp
from a_userauth.signals import send_verification_otp
from a_userauth.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class SendVerificationOTPView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user=request.user
        new_otp=generate_otp()
        # updating the otp
        EmailOTP.objects.filter(user=user).update(otp=new_otp, timestamp=timezone.now())
        send_verification_otp.send(sender=None, user=user)
        
        return Response({'message':'Otp sent successfully'})

        