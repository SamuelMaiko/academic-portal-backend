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
    
    @swagger_auto_schema(
        operation_description="Retrieve analytics data for a specific user by ID.",
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
                description="ID of the user for whom analytics data is to be retrieved.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Analytics data for the user",
                examples={
                    "application/json": {
                        "submitted_work": 1,
                        "words_written": 2000,
                        "assigned_work": 0,
                        "uptaken_work": 1,
                        "revoked_work": 3,
                        "quality_issues": 1
                    }
                }
            ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": "Account matching query does not exist."
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
        tags=['Accounts']
    )
    
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