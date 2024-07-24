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
                        "work_code": "W123",
                        "description": "Detailed description of the work",
                        "deadline": "2024-07-25T00:00:00Z",
                        "words": "example"
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