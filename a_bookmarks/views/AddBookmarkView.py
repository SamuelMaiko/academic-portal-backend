from django.db import IntegrityError
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from a_bookmarks.models import Bookmark
from a_work.models import Work


class AddBookmarkView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
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
