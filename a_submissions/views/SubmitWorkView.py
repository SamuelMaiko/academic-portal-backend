from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_submissions.serializers import SubmitWorkSerializer
from a_work.models import Work


class SubmitWorkView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, id):
        try:
            work=Work.objects.get(pk=id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
        data=request.data.copy()
        data["sender"]=request.user.id
        data["work"]=work.id
        serializer=SubmitWorkSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            
            if not work.is_submitted:
                work.is_submitted=True
                work.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)