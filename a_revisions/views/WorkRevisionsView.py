from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_revisions.serializers import RevisionSerializer
from a_work.models import Work


class WorkRevisionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            work= Work.objects.get(pk=id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        revisions=work.revisions
        serializer=RevisionSerializer(revisions, many=True, context={'request':request})
        return Response(serializer.data)