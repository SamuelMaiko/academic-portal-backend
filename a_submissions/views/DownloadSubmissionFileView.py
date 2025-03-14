from django.http import FileResponse
from django.shortcuts import get_object_or_404, render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from a_submissions.models import Submission


# Create your views here.
class DownloadSubmissionFileView(APIView):
    
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
    
    def get(self, request, submission_id):
        try:
            submission = Submission.objects.get(id=submission_id)
        except Submission.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)

        if not submission.file:
            return Response({'detail': 'Not found.'}, status=404)
    

        file_path = submission.file.path
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=submission.file.name)
        return response
