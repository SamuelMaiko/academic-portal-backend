from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_onboarding.serializers import OnboardingSerializer
from a_userauth.models import CustomUser


class Details(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve onboarding details of the authenticated user.",
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
                description="OK",
                examples={
                    "application/json": {
                        "email": "peterkenyatta631@gmail.com",
                        "first_name": "User",
                        "last_name": "Three",
                        "country": "",
                        "county": "",
                        "phone_number": ""
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
    
    def get(self, request):
        user=request.user
        serializer=OnboardingSerializer(user)

        return Response(serializer.data)