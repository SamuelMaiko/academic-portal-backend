from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.serializers import CreateAccountSerializer
from a_userauth.models import CustomUser
from a_work.permissions import IsAdmin


class CreateAccountView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def post(self, request):
        user=request.user
        self.check_object_permissions(request, user)

        serializer=CreateAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        