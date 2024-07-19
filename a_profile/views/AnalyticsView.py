from django.db.models import Q, Sum
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_work.models import DefaultWork


class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user=request.user
        no_submitted=user.submissions.values("work").distinct().count()
        words_written=user.submissions.values("work").distinct().aggregate(total_words=Sum("work__words"))["total_words"]
        assigned_work=user.assigned_work.count()
        uptaken_work=user.uptaken_work.count()
        revoked_work=user.default_work.filter(
            Q(type="RevokedUptaken") |
            Q(type="RevokedAssigned")
            ).count()

        quality_issues=user.default_work.filter(type="QualityIssues").count()
        data={
            "submitted_work":no_submitted,
            "words_written":words_written,
            "assigned_work":assigned_work,
            "uptaken_work":uptaken_work,
            "revoked_work":revoked_work,
            "quality_issues":quality_issues
        }
        return Response(data)