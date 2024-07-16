from rest_framework.views import APIView    
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from a_work.models import Work
from a_userauth.models import CustomUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from a_work.permissions import IsAdmin

class AssignWorkView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, id):
        writer=request.data.get('writer')
        if not writer:
            return Response({'error':'Provide writer'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            work=Work.objects.get(pk=id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        if work.has_writer:
            return Response({'error':'Work has already been allocated.'}, status=status.HTTP_400_BAD_REQUEST)
        # checking if has permission
        self.check_object_permissions(request, request.user)

        try:
            writer_to_assign=CustomUser.objects.get(pk=writer)
        except Work.DoesNotExist:
            return Response({'error':'user matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        work.assigned_to=writer_to_assign
        work.save()
        return Response({'message':'Work has been assigned successfully.'})
        
        