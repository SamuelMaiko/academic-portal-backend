from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_profile.serializers import UpdatePictureSerializer


class UpdatePictureView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
    operation_description="Update the profile picture of the authenticated user.",
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
            'profile_picture': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='File for the new profile picture',
                format=openapi.FORMAT_BINARY
            ),
        },
        required=['profile_picture']
    ),
    responses={
        200: openapi.Response(
            description="Profile picture updated successfully.",
            examples={
                "application/json": {
                    "profile_picture": "http://example.com/path/to/new/profile_picture.jpg"
                }
            }
        ),
        400: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    "profile_picture": [
                        "No file was submitted."
                    ]
                }
            }
        ),
        401: openapi.Response(
            description="Unauthorized",
            examples={
                "application/json": {
                    "detail": "Authentication credentials were not provided."
                }
            }
        )
    },
    tags=['Profile']
)
         
    def put(self, request):
        profile=request.user.profile
        serializer=UpdatePictureSerializer(profile,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            