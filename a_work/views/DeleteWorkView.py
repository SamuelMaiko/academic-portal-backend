from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_work.models import Work
from a_work.permissions import IsAdmin
from a_work.serializers import CreateWorkSerializer


class DeleteWorkView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin] 
    
    @swagger_auto_schema(
        operation_description="Delete a specific work.",
        responses={
            204: openapi.Response(
                description="No content, work successfully deleted"
            ),
            404: openapi.Response(
                description="Work not found",
                examples={
                    "application/json": {
                        "error": "Work matching query does not exist."
                    }
                }
            ),
        },
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description='ID of the work to be deleted.',
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        tags=['Work']
    )


    def delete(self, request, id, format=None):
        try:
            work= Work.objects.get(pk=id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
        self.check_object_permissions(request, request.user)
        work.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
