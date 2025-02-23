from django.http import FileResponse
from django.shortcuts import get_object_or_404, render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from cloudinary.utils import cloudinary_url

from a_work.models import WorkFile


# Create your views here.
class DownloadWorkFileView(APIView):
    
    @swagger_auto_schema(
        operation_description="Download a specific work file by its ID.",
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Bearer token for authentication',
                required=True
            ),
            openapi.Parameter(
                name='file_id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='ID of the work file to download',
                required=True
            )
        ],
        responses={
            200: 'file',
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "detail": "Not found."
                    }
                }
            ),
        },
        tags=['Work']
    )
    
    def get(self, request, file_id):
        try:
            file = WorkFile.objects.get(id=file_id)
        except WorkFile.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)

        # ✅ Generate proper Cloudinary URL with fl_attachment using the SDK
        download_url, options = cloudinary_url(
            file.file.name,  # Use the path as stored in Cloudinary
            resource_type="raw",
            attachment=True,  # Force download
        )

        return HttpResponseRedirect(download_url)
