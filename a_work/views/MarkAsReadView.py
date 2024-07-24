from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_work.models import Work
from a_work.permissions import IsWorkWriter


class MarkAsReadView(APIView):
    permission_classes = [IsAuthenticated, IsWorkWriter]

    def post(self, request, id):
        try:
            work= Work.objects.get(pk=id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, work)
        if not work.assigned_is_read:
            work.assigned_is_read=True
        if not work.uptaken_is_read:
            work.uptaken_is_read=True
        work.save()
        return Response({'message':'Work marked as read.'})
        
        