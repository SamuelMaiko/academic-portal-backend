from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_work.models import Work
from a_work.permissions import IsAdmin
from a_work.serializers import WorkSerializer


class BookmarksView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieve the list of bookmarks for the authenticated user.",
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
                description="List of bookmarks retrieved successfully",
                examples={
                    "application/json": [
                        {
                            "id": 9,
                            "work_code": "WK6809",
                            "deadline": "2024-08-01T17:30:00+03:00",
                            "words": 2500,
                            "type": "Essay",
                            "created_at": "2024-07-17T11:03:57.429099+03:00",
                            "is_bookmarked": True,
                            "has_writer": True,
                            "is_mine": False
                        },
                        {
                            "id": 6,
                            "work_code": "WK5506",
                            "deadline": "2024-07-17T15:00:00+03:00",
                            "words": 1500,
                            "type": "Essay",
                            "created_at": "2024-07-17T11:03:50.672897+03:00",
                            "is_bookmarked": True,
                            "has_writer": True,
                            "is_mine": False
                        },
                    ]
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
        tags=['Bookmarks']
    ) 

    def get(self, request):
        bookmarks=request.user.bookmarks
        serializer=WorkSerializer(bookmarks, many=True, context={'request':request})
        return Response(serializer.data)
