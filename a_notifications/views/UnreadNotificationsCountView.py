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