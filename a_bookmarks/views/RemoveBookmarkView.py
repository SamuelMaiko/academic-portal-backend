from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from a_bookmarks.models import Bookmark
from django.db import IntegrityError
from a_work.models import Work

class RemoveBookmarkView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, work_id):
        try:
            return Work.objects.get(id=work_id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'},status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, work_id):
        work=self.get_object(work_id)
        try:
            bookmark=Bookmark.objects.get(user=request.user, work=work)
        except Bookmark.DoesNotExist:
            return Response({'error':'bookmark for work does not exist.'},status=status.HTTP_404_NOT_FOUND)
        bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
