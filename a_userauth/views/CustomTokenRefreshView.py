from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView


class CustomTokenRefreshView(TokenRefreshView):
    
    @swagger_auto_schema(
        operation_description="Refresh JWT token (provide the refresh token and getting a new access token)",
        request_body=TokenRefreshSerializer,
        responses={
            200: openapi.Response(
                description="JWT token refreshed successfully",
                examples={
                    "application/json": {
                        "access": "new_access_token",
                        "refresh": "new_refresh_token"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": "Invalid token."
                    }
                }
            )
        },
        tags=['Authentication']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)