from rest_framework.views import APIView    
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from a_userauth.models import CustomUser
from a_onboarding.serializers import CompleteProfileSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CompleteProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        profile=request.user.profile
        serializer=CompleteProfileSerializer(profile, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            request.user.onboarding.profile_completed=True
            request.user.onboarding.save(update_fields=['profile_completed'])
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)