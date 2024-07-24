from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="""Logs out the user (does not do nothing because we are on stateless JWT). 
        This endpoint is intended for clients to handle token removal from their storage.""",
        responses={
            200: openapi.Response(
                description="Successful logout",
                examples={
                    "application/json": {
                        "message": "User logged out successfully"
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized",
                examples={
                    "application/json": {
                        "error": "Authentication credentials were not provided."
                    }
                }
            )
        },
        tags=['Authentication']
    )

    def post(self, request):
        # This endpoint is for the client to handle token removal
        return Response({"message":"User logged out successfully"}, status=status.HTTP_200_OK)
