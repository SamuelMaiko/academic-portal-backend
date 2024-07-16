from rest_framework.views import APIView    
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from a_userauth.models import CustomUser
from a_onboarding.serializers import OnboardingSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class Details(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user=request.user
        serializer=OnboardingSerializer(user)

        return Response(serializer.data)