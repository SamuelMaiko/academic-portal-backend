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
from a_work.permissions import IsAdmin


class AdminRevisionsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        user=request.user
        # check if admin
        self.check_object_permissions(request, user)
        # get revision where user is reviewer
        revisions=Revision.objects.filter(reviewer=user)
        # serialize
        serializer= RevisionSerializer(revisions, many=True, context={'request':request})
        return Response(serializer.data)