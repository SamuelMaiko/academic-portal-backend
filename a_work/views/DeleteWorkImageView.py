from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from a_work.models import WorkImage
from a_work.permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated

class DeleteWorkImageView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, image_id):
        try:
            image = WorkImage.objects.get(id=image_id)
            image.delete()
            return Response({"message": "Image deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except WorkImage.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
