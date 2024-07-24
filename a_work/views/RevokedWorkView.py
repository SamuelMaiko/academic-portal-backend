from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_userauth.models import CustomUser
from a_work.serializers import DefaultWorkSerializer


class RevokedWorkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user=request.user
        work=user.default_work.filter(
            Q(type="RevokedUptaken") |
            Q(type="RevokedAssigned")
            )
        serializer=DefaultWorkSerializer(work, many=True)
        return Response(serializer.data)