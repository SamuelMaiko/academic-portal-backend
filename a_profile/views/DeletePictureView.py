from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_profile.serializers import UpdatePictureSerializer


class DeletePictureView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
    operation_description="Delete the profile picture of the authenticated user.",
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
        204: openapi.Response(
            description="Profile picture deleted successfully."
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
         
    def delete(self, request):
        profile=request.user.profile
        profile.profile_picture=None
        profile.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
            