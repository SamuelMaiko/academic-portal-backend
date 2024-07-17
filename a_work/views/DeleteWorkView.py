from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from a_work.models import Work
from a_work.permissions import IsAdmin 
from a_work.serializers import CreateWorkSerializer  

class DeleteWorkView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin] 

    def get_object(self, pk):
        try:
            return Work.objects.get(pk=pk)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id, format=None):
        self.check_object_permissions(request, request.user)
        work = self.get_object(id)
        work.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
