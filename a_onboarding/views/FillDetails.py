from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_onboarding.serializers import OnboardingSerializer
from a_userauth.models import CustomUser


class FillDetails(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Update onboarding details for the authenticated user.",
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
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='Firstname of the user'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name of the user'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number of the user'),
                'country': openapi.Schema(type=openapi.TYPE_STRING, description='Country of the user'),
                'county': openapi.Schema(type=openapi.TYPE_STRING, description='County of the user'),
            },
            required=['first_name', 'last_name', 'phone_number','country','county']
        ),
        responses={
            200: openapi.Response(
                description="Details updated successfully.",
                examples={
                    "application/json": {
                        "email": "peterkenyatta631@gmail.com",
                        "first_name": "Peter",
                        "last_name": "K",
                        "country": "USA",
                        "county": "San Francisco",
                        "phone_number": "+1-987-654-3210"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "first_name": [
                            "This field is required."
                        ],
                        "last_name": [
                            "This field is required."
                        ],
                        "country": [
                            "This field is required."
                        ],
                        "county": [
                            "This field is required."
                        ],
                        "phone_number": [
                            "This field is required."
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
        tags=['Onboarding']
    )

    
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