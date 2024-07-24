from django.db.models import Exists, OuterRef, Q, Subquery
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_notifications.models import NotificationUser
from a_revisions.models import Revision, RevisionMessage
from a_submissions.models import Submission


class UnreadNotificationsCountView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieve counts of unread notifications, assigned work, uptaken work, and other relevant data for the authenticated user.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "assigned_work": 0,
                        "uptaken_work": 1,
                        "notifications": 0,
                        "revisions": 1,
                        "submissions": 7  # This will be included only if the user is an Admin
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
            )
        },
        tags=['Notifications']
    )
    
    def get(self, request):
        user=request.user
        assigned_work=user.assigned_work.filter(assigned_is_read=False).count()
        uptaken_work=user.uptaken_work.filter(uptaken_is_read=False).count()
        notifications=NotificationUser.objects.filter(user=request.user, is_read=False).count()
        submissions=Submission.objects.filter(is_claimed=False).count()
        is_read_subquery= RevisionMessage.objects.exclude(
            sender=request.user).filter(
            revision_id=OuterRef("id")
            , is_read=False
            )
        revisions=Revision.objects.annotate(is_read=Exists(is_read_subquery)).filter(is_read=False).count()
        
        data={
            "assigned_work":assigned_work,
            "uptaken_work":uptaken_work,
            "notifications":notifications,
            'revisions':revisions
        }
        if request.user.role=="Admin":
            data["submissions"]=submissions
        return Response(data)