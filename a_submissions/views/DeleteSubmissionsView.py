from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_submissions.models import Submission
from a_submissions.permissions import IsSubmissionSender
from a_submissions.serializers import SubmissionSerializer


class DeleteSubmissionsView(APIView):
    permission_classes = [IsAuthenticated, IsSubmissionSender]

    def delete(self, request, id):      
        try:
            submission=Submission.objects.get(pk=id)
        except Submission.DoesNotExist:
            return Response({'error':'submission matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, submission)
        submission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)