from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_profile.serializers import ContactInfoSerializer


class ContactInfoView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve the contact information of the authenticated user's profile.",
        responses={
            200: openapi.Response(
                description="Contact information retrieved successfully.",
                schema=ContactInfoSerializer,
                examples={
                    "application/json": {
                        "phone_number": "+1234567890",
                        "email": "user@example.com",
                        "address": "123 Main St, City, Country"
                    }
                }
            ),
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token for authentication",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        tags=['Profile']
    )
    
    def get(self, request):
        profile=request.user.profile
        serializer=ContactInfoSerializer(profile)
        return Response(serializer.data)