from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        pass
        # 