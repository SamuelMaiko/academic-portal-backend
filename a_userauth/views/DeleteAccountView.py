from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Deletes the authenticated user's account.",
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                description='Bearer token for authentication',
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Account successfully deleted",
                examples={
                    "application/json": {
                        "message": "Account deleted successfully"
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
            ),
        },
        tags=['Account Management']
    )
    
    def post(self, request):
        user = request.user
        user.delete()

        return Response({'message': 'Account deleted successfully'})