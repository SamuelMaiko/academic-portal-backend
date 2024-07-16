from rest_framework.views import APIView    
from rest_framework import status
from rest_framework.response import Response
from a_userauth.models import CustomUser
from a_profile.serializers import ProfileSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class Profile(APIView,):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        try:
            user=CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response({'error':'User matching query not found.'})

        profile=request.user.profile
        serializer=ProfileSerializer(profile)
        return Response(serializer.data)