from django.db.models import Q, Sum
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_userauth.models import CustomUser
from a_work.permissions import IsAdmin


class UserAnalyticsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request, id):
        self.check_object_permissions(request, request.user)
        
        try:
            account=CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response({'error':'account matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        no_submitted=account.submissions.values("work").distinct().count()
        words_written=account.submissions.values("work").distinct().aggregate(total_words=Sum("work__words"))["total_words"]
        assigned_work=account.assigned_work.count()
        uptaken_work=account.uptaken_work.count()
        revoked_work=account.default_work.filter(
            Q(type="RevokedUptaken") |
            Q(type="RevokedAssigned")
            ).count()

        quality_issues=account.default_work.filter(type="QualityIssues").count()
        data={
            "submitted_work":no_submitted,
            "words_written":words_written,
            "assigned_work":assigned_work,
            "uptaken_work":uptaken_work,
            "revoked_work":revoked_work,
            "quality_issues":quality_issues
        }
        return Response(data)