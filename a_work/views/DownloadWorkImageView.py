from a_work.models import Work, WorkImage
from django.http import FileResponse
from django.shortcuts import get_object_or_404, render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from cloudinary.utils import cloudinary_url

# Create your views here.
class DownloadWorkImageView(APIView):
    
    @swagger_auto_schema(
        operation_description="Download a specific work image by its ID.",
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Bearer token for authentication',
                required=True
            ),
            openapi.Parameter(
                name='image_id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='ID of the work image to download',
                required=True
            )
        ],
        responses={
            200: 'Image file',
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
    
    def get(self, request, image_id):
        try:
            image = WorkImage.objects.get(id=image_id)
        except WorkImage.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)

        # ✅ Force download using fl_attachment with a custom filename
        download_url, options = cloudinary_url(
            image.image.name,
            resource_type="image",
            transformation=[{'flags': 'attachment', 'fetch_format': 'auto'}],  # 👈 Forces download
            attachment=image.image.name  # ✅ Sets filename
        )

        return HttpResponseRedirect(download_url)
