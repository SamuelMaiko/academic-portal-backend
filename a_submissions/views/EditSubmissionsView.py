from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_submissions.models import Submission
from a_submissions.permissions import IsSubmissionSender
from a_submissions.serializers import SubmitWorkSerializer


class EditSubmissionsView(APIView):
    permission_classes = [IsAuthenticated, IsSubmissionSender]

    @swagger_auto_schema(
        operation_description="Edit a specific submission by ID. Accessible only by the sender of the submission.",
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
                description="ID of the submission to be edited.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['work','message',],
            properties={
                'work': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the work being submitted."),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description="Message accompanying the submission."),
                'file': openapi.Schema(type=openapi.TYPE_STRING, description="The file attached to the submission."),
            },
        ),
        responses={
            200: openapi.Response(
                description="Submission successfully updated.",
                examples={
                    "application/json": {
                        "id": 6,
                        "message": "Great yeah",
                        "file": "/media/submission_files/MyStudentSched_YIJwz0N.pdf",
                        "sender": 3,
                        "work": 4
                    }
                }
            ),
            404: openapi.Response(
                description="Submission not found.",
                examples={
                    "application/json": {
                        "error": "Submission matching query does not exist."
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
            401: openapi.Response(
                description="Unauthorized",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "work": ["This field is required."],
                        "message": ["This field is required."]
                    }
                }
            ),
        },
        tags=['Submissions']
    )

    def put(self, request, id):      
        try:
            submission=Submission.objects.get(pk=id)
        except Submission.DoesNotExist:
            return Response({'error':'submission matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, submission)

        serializer=SubmitWorkSerializer(submission,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)