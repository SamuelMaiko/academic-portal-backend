from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.serializers import AccountDetailSerializer
from a_userauth.models import CustomUser
from a_work.permissions import IsAdmin


class EditAccountView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @swagger_auto_schema(
        operation_description="Edit an existing account by ID.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the account to edit.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        request_body=AccountDetailSerializer,
        responses={
            200: openapi.Response(
                description="Account updated successfully",
                examples={
                    "application/json": {
                            "id": 1,
                            "profile_picture": "/media/profile_pics/Screenshot_2024-06-24_183856.png",
                            "first_name": "Sam",
                            "last_name": "Maiko",
                            "email": "sami@gmail.com",
                            "phone_number": "",
                            "country": "Kenya",
                            "county": "Nairobi",
                            "registration_number": "TW9801",
                            "role": "Admin",
                            "is_active": True,
                            "date_joined": "2024-07-17T10:59:38+03:00",
                            "last_login": "2024-07-24T09:48:44.302384+03:00",
                            "bio": ""
                        }
                }
            ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": "Account matching query does not exist."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "email": ["Enter a valid email address."],
                        "first_name": [
                            "This field is required."
                        ],
                        "last_name": [
                            "This field is required."
                        ]
                    }
                }
            ),
            403: openapi.Response(
                description="Permission Denied",
                examples={
                    "application/json": {
                        "detail": "You do not have permission to perform this action."
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
            ),
        },
        tags=['Accounts']
    )
    
    def put(self, request,id):
        user=request.user
        self.check_object_permissions(request, user)

        try:
            account=CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response({'error':'account matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer=AccountDetailSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        