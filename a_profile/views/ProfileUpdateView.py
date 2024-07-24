from rest_framework.views import APIView    
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from a_profile.serializers import ProfileUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile=request.user.profile
        serializer=ProfileUpdateSerializer(profile)
        return Response(serializer.data)
            
    def put(self, request):
        profile=request.user.profile
        serializer=ProfileUpdateSerializer(profile,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            