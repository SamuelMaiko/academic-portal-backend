from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from a_work.models import Work, WorkImage
from a_work.serializers import WorkImageSerializer
from a_work.permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated

class WorkImageUploadView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, work_id):
        images = request.FILES.getlist("images")

        if not images:
            return Response({"error": "No images uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            work = Work.objects.get(id=work_id)
        except Work.DoesNotExist:
            return Response({"error": "Work not found"}, status=status.HTTP_404_NOT_FOUND)


        # Bulk create WorkImage instances
        work_images = [WorkImage(work=work, image=image) for image in images]
        WorkImage.objects.bulk_create(work_images)

        serializer = WorkImageSerializer(work_images, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
