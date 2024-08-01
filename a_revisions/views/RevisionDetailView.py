from a_revisions.models import Revision
from a_revisions.serializers import RevisionDetailSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class RevisionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
    operation_description="Retrieve the details of a specific revision by its ID. NOTE: Updates opened_by_writer and opened_by_reviewer variables.",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer token",
            type=openapi.TYPE_STRING,
            required=True
        ),
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="ID of the revision to retrieve.",
            type=openapi.TYPE_INTEGER,
            required=True
        ),
    ],
    responses={
        200: openapi.Response(
            description="Details of the specified revision.",
            examples={
                "application/json": {
                    "id": 3,
                    "submit_before": "2024-08-01T17:30:00+03:00",
                    "status": "Not started",
                    "reviewer": {
                        "id": 1,
                        "registration_number": "TW9801",
                        "first_name": "Sam",
                        "last_name": "Maiko"
                    },
                    "messages": [
                        {
                            "id": 32,
                            "message": "Correct now :laughy",
                            "emoji_message": "Correct now😂",
                            "file": None,
                            "image": None,
                            "file_download_link": "http://localhost:8000/api/work/download/1/",
                            "image_download_link": "http://localhost:8000/api/work/download/1/",
                            "is_read": True,
                            "sender": {
                                "id": 1,
                                "registration_number": "TW9801",
                                "first_name": "Sam",
                                "last_name": "Maiko"
                            },
                            "revision": 3,
                            "is_mine": True,
                            "created_at": "2024-07-19T17:58:30.105506+03:00"
                        },
                        {
                            "id": 33,
                            "message": "Correct :laughy",
                            "emoji_message": "Correct now😂",
                            "file": None,
                            "image": None,
                            "file_download_link": "http://localhost:8000/api/work/download/1/",
                            "image_download_link": "http://localhost:8000/api/work/download/1/",
                            "is_read": True,
                            "sender": {
                                "id": 3,
                                "registration_number": "TW5303",
                                "first_name": "Peter",
                                "last_name": "K"
                            },
                            "revision": 3,
                            "is_mine": False,
                            "created_at": "2024-07-19T18:12:08.967059+03:00"
                        }
                    ]
                }
            }
        ),
        404: openapi.Response(
            description="Revision Not Found",
            examples={
                "application/json": {
                    "error": "Revision matching query does not exist."
                }
            }
        ),
        401: openapi.Response(
            description="Unauthorized",
            examples={
                "application/json": {
                    "detail": "Authentication credentials were not provided."
                }
            }
        )
    },
    tags=['Revisions']
)

    def get(self, request, id):
        try:
            revision = Revision.objects.get(pk=id)
        except Revision.DoesNotExist:
            return Response({'error': 'Revision matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = RevisionDetailSerializer(revision, context={'request': request})

        # update the status
        if request.user.role=='Writer' and not revision.opened_by_writer :
            revision.opened_by_writer=True
            revision.status="In Progress"
            revision.save(update_fields=["opened_by_writer","status"])

        if request.user.role=='Admin' and not revision.opened_by_reviewer :
            revision.opened_by_reviewer=True
            revision.save(update_fields=["opened_by_reviewer"])

        return Response(serializer.data, status=status.HTTP_200_OK)
