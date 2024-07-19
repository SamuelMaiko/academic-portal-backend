from django.db.models import Subquery
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_submissions.models import Submission
from a_submissions.serializers import SubmittedWorkSerializer
from a_work.models import Work


class MySubmittedWorkView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user=request.user        
        sub_work=Submission.objects.filter(sender=user).order_by("-created_at").values("work_id").distinct().values_list("work_id", flat=True)
        
        submitted_work=Work.objects.filter(id__in=sub_work)
        serializer=SubmittedWorkSerializer(submitted_work, many=True, context={'user':user})
        return Response(serializer.data)