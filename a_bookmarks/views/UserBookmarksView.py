from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_userauth.models import CustomUser
from a_work.models import Work
from a_work.permissions import IsAdmin
from a_work.serializers import WorkSerializer


class UserBookmarksView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin] 
    
    @swagger_auto_schema(
        operation_description="Retrieve the bookmarks of a specific user by ID.",
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
                description="ID of the user whose bookmarks are to be retrieved.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="List of bookmarks for the user",
                examples={
                    "application/json": [
                        {
                            "id": 9,
                            "work_code": "WK6809",
                            "deadline": "2024-08-01T17:30:00+03:00",
                            "words": 2500,
                            "type": "Essay",
                            "created_at": "2024-07-17T11:03:57.429099+03:00",
                            "is_bookmarked": False,
                            "has_writer": True,
                            "is_mine": True
                        },
                        {
                            "id": 6,
                            "work_code": "WK5506",
                            "deadline": "2024-07-17T15:00:00+03:00",
                            "words": 1500,
                            "type": "Essay",
                            "created_at": "2024-07-17T11:03:50.672897+03:00",
                            "is_bookmarked": False,
                            "has_writer": True,
                            "is_mine": True
                        },
                    ]
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

    def get(self, request, id):
        self.check_object_permissions(request, request.user)

        try:
            account=CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response({'error':'account matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        bookmarks=account.bookmarks
        serializer=WorkSerializer(bookmarks, many=True, context={'request':request})
        return Response(serializer.data)
