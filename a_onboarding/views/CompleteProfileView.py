from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_onboarding.serializers import CompleteProfileSerializer
from a_userauth.models import CustomUser


class CompleteProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Complete user profile information.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'profile_picture': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                'bio': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['bio']  # bio is required
        ),
        responses={
            200: openapi.Response(
                description="Profile updated successfully.",
                examples={
                    "application/json": {
                        "profile_picture": "https://example.com/profile.jpg",
                        "bio": "This is a bio.",
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "bio": ["This field is required."]
                    }
                }
            ),
        },
        tags=['Onboarding']
    )
    
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