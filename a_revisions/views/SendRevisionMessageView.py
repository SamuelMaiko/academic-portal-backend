from a_accounts.helpers import get_admins
from a_notifications.models import Notification
from a_revisions.models import Revision
from a_revisions.serializers import RevisionMessageSerializer
from a_work.models import Work
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class SendRevisionMessageView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Send a message related to a specific revision by ID.",
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
                description="ID of the revision to add the message to.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Message content'),
                'file': openapi.Schema(type=openapi.TYPE_STRING, description='Optional file', format='binary'),
                'image': openapi.Schema(type=openapi.TYPE_STRING, description='Optional image', format='binary'),
            },
            required=['message']
        ),
        responses={
            200: openapi.Response(
                description="Message successfully sent.",
                examples={
                    "application/json": {
                        "id": 35,
                        "message": "Great :glassy",
                        "emoji_message": "Great😎",
                        "file": None,
                        "image": "http://localhost:8000/media/revision_message_images/wallpaperflare.com_wallpaper_1.jpg",
                        "is_read": False,
                        "sender": {
                            "id": 1,
                            "registration_number": "TW9801",
                            "first_name": "Sam",
                            "last_name": "Maiko"
                        },
                        "revision": 3,
                        "is_mine": True,
                        "created_at": "2024-07-24T14:36:36.718029+03:00"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "message": ["This field is required."]
                    }
                }
            ),
            404: openapi.Response(
                description="Not Found",
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
            ),
        },
        tags=['Revisions']
    )

    def post(self, request,id):
        try:
            revision = Revision.objects.get(pk=id)
        except Revision.DoesNotExist:
            return Response({'error': 'Revision matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        data=request.data.copy()
        data['sender']=request.user
        data["revision"]=revision.id

        serializer=RevisionMessageSerializer(data=data, context={'request':request})
        if serializer.is_valid():
            # print("Serializer is valid")
            serializer.save(sender=request.user)
            return Response(serializer.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)