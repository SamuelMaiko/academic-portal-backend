from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from a_work.models import Work
from a_work.permissions import IsAdmin  # Adjust import as per your actual permissions setup
from a_work.serializers import CreateWorkSerializer  # Adjust serializer as needed

class EditWorkView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]  # Adjust permissions as needed

    def get_object(self, pk):
        try:
            return Work.objects.get(pk=pk)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id, format=None):
        self.check_object_permissions(request, request.user)
        work = self.get_object(id)
        serializer = CreateWorkSerializer(work, data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        self.check_object_permissions(request, request.user)
        work = self.get_object(pk)
        work.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
