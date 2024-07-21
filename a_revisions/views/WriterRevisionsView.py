from django.db.models import Q, Subquery
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_notifications.models import Notification
from a_revisions.models import Revision
from a_revisions.serializers import RevisionSerializer
from a_work.models import Work


class WriterRevisionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # get the user
        user=request.user
        # get work he is the writer(assigned or uptaken)
        work_subquery=Work.objects.filter(Q(assigned_to=user) | Q(uptaken_by=user)).values_list('id',flat=True)
        # take only revisions where the writer's work is revised
        revisions=Revision.objects.filter(work_id__in=Subquery(work_subquery))
        serializer= RevisionSerializer(revisions, many=True, context={'request':request})
        return Response(serializer.data)
    