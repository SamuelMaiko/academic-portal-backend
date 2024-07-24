from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_preferences.serializers import PreferenceSerializer


class PreferencesView(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve user preferences.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token for authentication",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="User preferences retrieved successfully.",
                examples={
                    "application/json": {
                        "dark_mode": True
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
        tags=['Preferences']
    )

    def get(self, request):
        preferences=request.user.preferences
        serializer=PreferenceSerializer(preferences)
        return Response(serializer.data)