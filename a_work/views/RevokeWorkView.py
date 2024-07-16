from rest_framework.views import APIView    
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from a_work.models import Work
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RevokeWorkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            work=Work.objects.get(pk=id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user!=work.writer:
            return Response({'error':'work not found in list of allocated work.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if work.uptaken_by is None:
            # means it was assigned
            work.assigned_to=None
        else:
            # means it was uptaken
            work.uptaken_by=None
        
        work.save()
        return Response({'message':'Work has been revoked successfully.'})
        
        