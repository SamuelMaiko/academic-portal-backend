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
    
    @swagger_auto_schema(
        operation_description="Retrieve analytics data for the authenticated user.",
        responses={
            200: openapi.Response(
                description="Analytics data retrieved successfully.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'submitted_work': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of submitted works'),
                        'words_written': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total words written'),
                        'assigned_work': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of assigned works'),
                        'uptaken_work': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of uptaken works'),
                        'revoked_work': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of revoked works'),
                        'quality_issues': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of quality issues')
                    },
                    example={
                        'submitted_work': 5,
                        'words_written': 1200,
                        'assigned_work': 3,
                        'uptaken_work': 2,
                        'revoked_work': 1,
                        'quality_issues': 0
                    }
                )
            ),
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token for authentication",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        tags=['Profile']
    )

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