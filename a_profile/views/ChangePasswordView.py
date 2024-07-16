from rest_framework.views import APIView    
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from a_userauth.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from a_profile.serializers import ChangePasswordSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            # Check if the old password is correct
            if not check_password(old_password, user.password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if the new password is the same as the old password
            if old_password == new_password:
                return Response({"new_password": ["New password cannot be the same as the old password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # Set the new password
            user.set_password(new_password)
            user.save()
            
            user.onboarding.password_changed=True
            user.onboarding.save()

            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            