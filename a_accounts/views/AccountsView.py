from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.serializers import AccountSerializer
from a_userauth.models import CustomUser
from a_work.permissions import IsAdmin


class AccountsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        user=request.user
        self.check_object_permissions(request, user)
        
        users=CustomUser.objects.exclude(id=user.id).order_by('-created_at')
        serializer=AccountSerializer(users, many=True)
        return Response(serializer.data)
        