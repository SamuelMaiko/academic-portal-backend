from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from a_work.models import Work
from a_work.permissions import IsAdmin  
from a_work.serializers import WorkSerializer

class BookmarksView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        bookmarks=request.user.bookmarks
        serializer=WorkSerializer(bookmarks, many=True, context={'request':request})
        return Response(serializer.data)
