from rest_framework.views import APIView    
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from a_work.models import Work
from a_work.serializers import WorkDetailSerializer
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class WorkDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            work=Work.objects.get(pk=id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
        serializer=WorkDetailSerializer(work, context={'request':request})
        return Response(serializer.data)