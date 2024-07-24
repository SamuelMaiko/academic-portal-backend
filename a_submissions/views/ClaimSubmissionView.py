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
from a_work.permissions import IsAdmin


class ClaimSubmissionView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def post(self, request, id):
        self.check_object_permissions(request, request.user)

        try:
            submission=Submission.objects.get(pk=id)
        except Submission.DoesNotExist:
            return Response({'error':'submission matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        user=request.user        
        if submission.is_claimed:
            return Response({'error':'submission already claimed.'}, status=status.HTTP_400_BAD_REQUEST)
        
        submission.claimed_by=request.user
        submission.is_claimed=True
        submission.save()
        return Response({'message':'submission claimed successfully.'})