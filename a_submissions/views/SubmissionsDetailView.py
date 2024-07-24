from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_submissions.models import Submission
from a_submissions.serializers import SubmissionSerializer


class SubmissionsDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):      
        try:
            submission=Submission.objects.get(pk=id)
        except Submission.DoesNotExist:
            return Response({'error':'submission matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        submission=self.get_object(id)
        serializer=SubmissionSerializer(submission)
        return Response(serializer.data)