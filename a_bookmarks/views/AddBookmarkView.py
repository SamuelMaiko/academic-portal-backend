from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from a_bookmarks.models import Bookmark
from django.db import IntegrityError
from a_work.models import Work

class AddBookmarkView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, work_id):
        try:
            return Work.objects.get(id=work_id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
    def post(self, request, work_id):
        work=self.get_object(work_id)
        try:
            Bookmark.objects.create(user=request.user, work=work)
        except IntegrityError:
            return Response({'error':'bookmark already exists.'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'work bookmarked successfully.'})
