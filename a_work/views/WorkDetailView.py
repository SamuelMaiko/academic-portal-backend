from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_work.models import Work
from a_work.serializers import WorkDetailSerializer


class WorkDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieves the details of a specific work item by its ID.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description='ID of the work to retrieve details.',
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Details of the work item",
                examples={
                    "application/json": {
                            "id": 1,
                            "work_code": "WK5201",
                            "type": "Reflection Paper",
                            "deadline": "2024-07-26T19:02:13+03:00",
                            "words": 2500,
                            "status": "Not started",
                            "comment": "Works",
                            "created_at": "2024-07-17T11:03:30.872580+03:00",
                            "is_bookmarked": False,
                            "has_writer": False,
                            "is_mine": False,
                            "images": [
                                {
                                    "id": 1,
                                    "image": "http://localhost:8000/media/work_images/wallpaperflare.com_wallpaper.jpg",
                                    "image_name": "wallpaperflare.com_wallpaper",
                                    "image_extension": "jpg",
                                    "combined": "wallpaperflare.com_wallpaper.jpg",
                                    "download_url": "http://localhost:8000/api/work/download/1/"
                                },
                                {
                                    "id": 2,
                                    "image": "http://localhost:8000/media/work_images/wallpaperflare.com_wallpaper_1.jpg",
                                    "image_name": "wallpaperflare.com_wallpaper_1",
                                    "image_extension": "jpg",
                                    "combined": "wallpaperflare.com_wallpaper_1.jpg",
                                    "download_url": "http://localhost:8000/api/work/download/2/"
                                }
                            ],
                            "files": [
                                {
                                    "id": 1,
                                    "file_name": "MyStudentSched.pdf",
                                    "file": "http://localhost:8000/media/work_files/MyStudentSched.pdf",
                                    "download_url": "http://localhost:8000/api/work/download/1/"
                                },
                                {
                                    "id": 2,
                                    "file_name": "images_1.zip",
                                    "file": "http://localhost:8000/media/work_files/images_1.zip",
                                    "download_url": "http://localhost:8000/api/work/download/1/"
                                },
                                {
                                    "id": 3,
                                    "file_name": "pcnema-windows.exe",
                                    "file": "http://localhost:8000/media/work_files/pcnema-windows.exe",
                                    "download_url": "http://localhost:8000/api/work/download/1/"
                                }
                            ],
                            "writer": None,
                            "images_zip_url": "http://localhost:8000/api/work/download-images/1/"
                        }
                }
            ),
            404: openapi.Response(
                description="Work item not found",
                examples={
                    "application/json": {
                        "error": "work matching query does not exist."
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized",
                examples={
                    "application/json": {
                        "error": "Authentication credentials were not provided."
                    }
                }
            ),
        },
        tags=['Work']
    )

    def get(self, request, id):
        try:
            work=Work.objects.get(pk=id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
        serializer=WorkDetailSerializer(work, context={'request':request})
        return Response(serializer.data)