from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.serializers import AccountDetailSerializer
from a_userauth.models import CustomUser
from a_work.permissions import IsAdmin


class AccountDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request, id):
        user=request.user
        self.check_object_permissions(request, user)

        try:
            account=CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response({'error':'account matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer=AccountDetailSerializer(account)
        return Response(serializer.data)
        