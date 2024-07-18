from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_revisions.models import Revision
from a_revisions.serializers import RevisionDetailSerializer


class RevisionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            revision = Revision.objects.get(pk=id)
        except Revision.DoesNotExist:
            return Response({'error': 'Revision matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = RevisionDetailSerializer(revision, context={'request': request})

        # update the status
        if request.user.role=='Writer' and not revision.opened_by_writer :
            revision.opened_by_writer=True
            revision.save()

        if request.user.role=='Admin' and not revision.opened_by_reviewer :
            revision.opened_by_reviewer=True
            revision.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
