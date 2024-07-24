from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_profile.serializers import ProfileSerializer


class MyProfile(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieve the authenticated user's profile information.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Profile data retrieved successfully.",
                schema=ProfileSerializer,
                examples={
                    "application/json": {
                            "profile_picture": "/media/profile_pics/Screenshot_2024-06-24_183856.png",
                            "bio": "",
                            "first_name": "Sam",
                            "last_name": "Maiko",
                            "registration_number": "TW9801",
                            "country": "Kenya",
                            "county": "Nairobi"
                        }
                }
            ),
            401: openapi.Response(
                description="Unauthorized access",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
        },
        tags=['Profile']
    )

    
    def get(self, request):
        profile=request.user.profile
        serializer=ProfileSerializer(profile)
        return Response(serializer.data)