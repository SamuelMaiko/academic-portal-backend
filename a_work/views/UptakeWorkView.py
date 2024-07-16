from rest_framework.views import APIView    
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from a_work.models import Work
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UptakeWorkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            work=Work.objects.get(pk=id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        if work.has_writer:
            return Response({'error':'Work has already been allocated.'}, status=status.HTTP_400_BAD_REQUEST)

        work.uptaken_by=request.user
        work.save()
        return Response({'message':'Work has been uptaken successfully.'})
        
        