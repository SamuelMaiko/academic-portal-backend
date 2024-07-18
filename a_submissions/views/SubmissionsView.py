from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_submissions.models import Submission
from a_submissions.serializers import SubmissionSerializer
from a_work.models import Work


class SubmissionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user=request.user        
        submissions=Submission.objects.filter(sender=user)
        serializer=SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)