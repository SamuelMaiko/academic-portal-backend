import io
import zipfile
import requests
import os

from a_work.models import Work
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from cloudinary.utils import cloudinary_url
import mimetypes


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

    def get(self, request, work_id):
        try:
            work = Work.objects.get(id=work_id)
        except Work.DoesNotExist:
            return Response({'error': 'Work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        images = work.images.all()
        buffer = io.BytesIO()

        with zipfile.ZipFile(buffer, 'w') as zip_file:
            for idx, image in enumerate(images, start=1):
                image_url = image.image.url
                print(f"Fetching image from URL: {image_url}")

                try:
                    response = requests.get(image_url, stream=True)
                    print(f"Status code: {response.status_code}")

                    if response.status_code == 200:
                        content_type = response.headers.get('Content-Type', '')
                        extension = mimetypes.guess_extension(content_type) or ".jpg"
                        filename = f"image_{idx}{extension}"
                        print(f"Saving as: {filename} ({content_type})")

                        zip_file.writestr(filename, response.content)
                    else:
                        print(f"Failed to download {image_url}. Status: {response.status_code}")
                except Exception as e:
                    print(f"Exception while downloading image: {str(e)}")

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="images_{work.work_code}.zip"'
        return response