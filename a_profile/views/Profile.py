from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_profile.serializers import ProfileSerializer
from a_userauth.models import CustomUser


class Profile(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieve the profile information of a specific user by their ID.",
        manual_parameters=[
            openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer token",
            type=openapi.TYPE_STRING,
            required=True
            ),

            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='ID of the user whose profile is to be retrieved.'
            )
        ],
        responses={
            200: openapi.Response(
                description="Profile data retrieved successfully.",
                schema=ProfileSerializer,
                examples={
                    "application/json": {
                        "profile_picture": "https://example.com/path/to/profile_picture.jpg",
                        "bio": "This is the user's bio",
                        "phone_number": "+1234567890",
                        "location": "City, Country",
                    }
                }
            ),
            404: openapi.Response(
                description="User not found.",
                examples={
                    "application/json": {
                        "error": "User matching query not found."
                    }
                }
            ),
        },
        tags=['Profile']
    )
    
    def get(self, request, id):
        try:
            user=CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response({'error':'User matching query not found.'})

        profile=request.user.profile
        serializer=ProfileSerializer(profile)
        return Response(serializer.data)