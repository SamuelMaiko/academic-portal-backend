from rest_framework.views import APIView    
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from a_work.models import Work
from a_work.serializers import WorkSerializer
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class WorkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # removing the assigned and uptaken work
        work=Work.objects.filter(Q(uptaken_by=None) & Q(assigned_to=None)).all()
        serializer=WorkSerializer(work, many=True, context={'request':request})
        return Response(serializer.data)