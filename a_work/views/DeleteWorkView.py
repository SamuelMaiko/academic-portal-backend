from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_work.models import Work
from a_work.permissions import IsAdmin
from a_work.serializers import CreateWorkSerializer


class DeleteWorkView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin] 


    def delete(self, request, id, format=None):
        try:
            work= Work.objects.get(pk=id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
        self.check_object_permissions(request, request.user)
        work.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
