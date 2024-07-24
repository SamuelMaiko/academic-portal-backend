from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_preferences.serializers import PreferenceSerializer


class PreferenceUpdateView(APIView):
    permission_classes=[IsAuthenticated]  
    
    @swagger_auto_schema(
        operation_description="Update user preferences.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'dark_mode': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="theme true or false"),
            },
            required=['dark_mode',], 
        ),
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
                description="Preferences updated successfully.",
                examples={
                    "application/json": {
                        "dark_mode": True

                    }
                }
            ),
            400: openapi.Response(
                description="Invalid data",
                examples={
                    "application/json": {
                        "dark_mode": [
                            "This field is required."
                        ]
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
    
    def put(self, request):
        preferences=request.user.preferences
        serializer=PreferenceSerializer(preferences, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)