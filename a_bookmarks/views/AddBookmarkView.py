from django.db import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from a_bookmarks.models import Bookmark
from a_work.models import Work


class AddBookmarkView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Add a bookmark for a specific work.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'work_id',
                openapi.IN_PATH,
                description="ID of the work to be bookmarked.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Work bookmarked successfully",
                examples={
                    "application/json": {
                        "message": "Work bookmarked successfully."
                    }
                }
            ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": "Work matching query does not exist."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": "Bookmark already exists."
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
        tags=['Bookmarks']
    )
    
    def post(self, request, work_id):
        try:
            work= Work.objects.get(id=work_id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            Bookmark.objects.create(user=request.user, work=work)
        except IntegrityError:
            return Response({'error':'bookmark already exists.'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'work bookmarked successfully.'})
