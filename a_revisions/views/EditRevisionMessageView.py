from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_revisions.models import RevisionMessage
from a_revisions.permissions import IsRevisionMessageSender
from a_revisions.serializers import RevisionMessageSerializer


class EditRevisionMessageView(APIView):
    permission_classes = [IsAuthenticated, IsRevisionMessageSender]
    
    @swagger_auto_schema(
        operation_description="Edit a specific revision message by ID.",
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
                description="ID of the revision message to be edited.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='The content of the revision message'),
                'file': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_BINARY, description='Optional file attachment'),
                'image': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_BINARY, description='Optional image attachment'),
            },
            required=['message'],
        ),
        responses={
            200: openapi.Response(
                description="Revision message updated successfully.",
                examples={
                    "application/json": {
                        "id": 35,
                        "message": "Great yeah",
                        "file": None,
                        "image": "http://localhost:8000/media/revision_message_images/ResetPassword.png",
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
                        "error": "revision message matching query does not exist."
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
            403: openapi.Response(
                description="Permission Denied",
                examples={
                    "application/json": {
                        "detail": "You do not have permission to perform this action."
                    }
                }
            ),
        },
        tags=['Revisions']
    )

    def put(self, request, id):      
        try:
            revision_message=RevisionMessage.objects.get(pk=id)
        except RevisionMessage.DoesNotExist:
            return Response({'error':'revision message matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        # checking permissions
        self.check_object_permissions(request, revision_message)

        data=request.data.copy()
        data["revision"]=revision_message.revision.id
        data["sender"]=revision_message.sender.id
        serializer=RevisionMessageSerializer(revision_message,data=data, context={'request':request})
        if serializer.is_valid():
            serializer.save(sender=revision_message.sender)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)