from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_submissions.serializers import SubmitWorkSerializer
from a_work.models import Work


class SubmitWorkView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Submit work by sending the work ID and submission details.",
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Bearer token for authentication',
                required=True
            ),
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='ID of the work being submitted',
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['message','file'],
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description="Message accompanying the submission."),
                'file': openapi.Schema(type=openapi.TYPE_STRING, description="The file attached to the submission."),
            },
        ),
        responses={
            200: openapi.Response(
                description="Work submitted successfully",
                examples={
                    "application/json": {
                        "id": 9,
                        "message": "Great yeah",
                        "file": "/media/submission_files/MyStudentSched_GKfbnat.pdf",
                        "sender": 3,
                        "work": 1
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "message": [
                            "This field is required."
                        ]
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
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": "Work matching query does not exist."
                    }
                }
            )
        },
        tags=['Work']
    )
    
    def post(self, request, id):
        try:
            work=Work.objects.get(pk=id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
        data=request.data.copy()
        data["sender"]=request.user.id
        data["work"]=work.id
        serializer=SubmitWorkSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            
            if not work.is_submitted:
                work.is_submitted=True
                work.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)