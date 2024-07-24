from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_submissions.models import Submission
from a_submissions.serializers import AllSubmissionsSerializer
from a_work.models import Work
from a_work.permissions import IsAdmin


class AllSubmissionsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        self.check_object_permissions(request, request.user)

        submissions=Submission.objects.all()
        serializer=AllSubmissionsSerializer(submissions, many=True, context={'request':request})
        return Response(serializer.data)