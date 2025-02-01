from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from a_work.models import WorkFile
from a_work.permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated

class DeleteWorkFileView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, file_id):
        try:
            file = WorkFile.objects.get(id=file_id)
            file.delete()
            return Response({"message": "File deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except WorkFile.DoesNotExist:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
