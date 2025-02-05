from django.db.models import Q, Sum
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_work.models import DefaultWork, Work
from a_userauth.models import CustomUser


class GeneralAccountAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        writers_employed=CustomUser.objects.filter(role="Writer").count()
        work_completed=Work.objects.filter(is_submitted=True).count()
        words_written=Work.objects.filter(is_submitted=True).aggregate(total_words=Sum("words"))["total_words"] or 0
        poor_work=DefaultWork.objects.filter(type="QualityIssues").count()
        data={
            "writers_employed":writers_employed,
            "work_completed":work_completed,
            "words_written":words_written,
            "poor_work":poor_work,
        }
        
        return Response(data)