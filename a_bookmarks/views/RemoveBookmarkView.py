from django.db import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from a_bookmarks.models import Bookmark
from a_work.models import Work


class RemoveBookmarkView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Remove a bookmark for a specific work.",
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
                description="ID of the work to be removed from bookmarks.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            204: openapi.Response(
                description="Bookmark removed successfully"
            ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": "Work matching query does not exist or bookmark does not exist."
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

    def delete(self, request, work_id):
        try:
            work= Work.objects.get(id=work_id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            bookmark=Bookmark.objects.get(user=request.user, work=work)
        except Bookmark.DoesNotExist:
            return Response({'error':'bookmark for work does not exist.'},status=status.HTTP_404_NOT_FOUND)
        bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
