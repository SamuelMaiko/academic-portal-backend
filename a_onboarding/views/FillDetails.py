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

class FillDetails(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        user=request.user
        serializer=OnboardingSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            user.onboarding.details_filled=True
            user.onboarding.save(update_fields=['details_filled'])
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)