from django.db import IntegrityError
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from a_bookmarks.models import Bookmark
from a_work.models import Work


class RemoveBookmarkView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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
