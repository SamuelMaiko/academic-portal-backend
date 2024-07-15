from rest_framework.views import APIView    
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from a_userauth.models import EmailOTP
from a_userauth.HelperFunctions import generate_otp
from a_userauth.signals import send_otp_signal
from a_userauth.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        user.delete()

        return Response({'message': 'Account deleted successfully'})