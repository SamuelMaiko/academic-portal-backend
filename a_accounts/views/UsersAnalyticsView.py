from django.db.models import Q, Sum
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from a_userauth.models import CustomUser
from a_accounts.serializers import UsersAnalyticsSerializer

from a_work.models import DefaultWork


class UsersAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        all_writers= CustomUser.objects.filter(role="Writer").all()
        serializer = UsersAnalyticsSerializer(all_writers, many=True)
        
        return Response(serializer.data)