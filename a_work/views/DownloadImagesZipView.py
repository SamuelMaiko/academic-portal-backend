import io
import zipfile

from a_work.models import Work
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class DownloadImagesZipView(APIView):

    @swagger_auto_schema(
        operation_description="Download all images associated with a specific work as a ZIP file.",
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Bearer token for authentication',
                required=True
            ),
            openapi.Parameter(
                name='work_id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='ID of the work whose images will be downloaded',
                required=True
            )
        ],
        responses={
            200: 'ZIP file containing images',
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": "work matching query does not exist."
                    }
                }
            ),
        },
        tags=['Work']
    )

    def get(self,request, work_id):
        try:
            work = Work.objects.get(id=work_id)
        except Work.DoesNotExist:
            return Response({'error': 'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        images = work.images.all()

        # Create a byte stream to hold the zip file
        buffer = io.BytesIO()
        
        # Create a zip file in memory
        with zipfile.ZipFile(buffer, 'w') as zip_file:
            for image in images:
                image_path = image.image.path
                image_name = image.image.name
                zip_file.write(image_path, arcname=image_name)

        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="images_{work.work_code}.zip"'
        return response
