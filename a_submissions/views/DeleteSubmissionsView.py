from a_submissions.models import Submission
from a_submissions.permissions import IsSubmissionSender
from a_submissions.serializers import SubmissionSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class DeleteSubmissionsView(APIView):
    permission_classes = [IsAuthenticated, IsSubmissionSender]
    
    @swagger_auto_schema(
        operation_description="Delete a specific submission by ID. Accessible only by the sender of the submission.",
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
                description="ID of the submission to be deleted.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            204: openapi.Response(
                description="Submission successfully deleted."
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
        },
        tags=['Submissions']
    )

    def delete(self, request, id):      
        try:
            submission=Submission.objects.get(pk=id)
        except Submission.DoesNotExist:
            return Response({'error':'submission matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, submission)
        submission.delete()
        
        # updating work to not submitted and changing progress
        submission.work.is_submitted=False
        submission.work.status="In Progress"
        submission.work.save(update_fields=["is_submitted","status"])
        return Response(status=status.HTTP_204_NO_CONTENT)