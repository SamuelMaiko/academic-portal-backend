from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_work.models import DefaultWork, Work


class RevokeWorkView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Revokes work the user has been assigned or has uptaken. NOTE: The work is added to the user's default work",
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description='Bearer token for authentication',
                required=True
            ),
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='ID of the work to revoke',
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Success",
                examples={
                    "application/json": {
                        "message": "Work has been revoked successfully."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": "Work not found in list of allocated work."
                    }
                }
            ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": "Work matching query does not exist."
                    }
                }
            ),
        },
        tags=['Work']
    )

    def post(self, request, id):
        try:
            work=Work.objects.get(pk=id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user!=work.writer:
            return Response({'error':'work not found in list of allocated work.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if work.uptaken_by is None:
            # means it was assigned
            work.assigned_to=None
            DefaultWork.objects.create(
                user=request.user,
                work=work,
                type="RevokedAssigned"
                )
            # SET WORK to unread
            work.assigned_is_read=False
        else:
            # means it was uptaken
            work.uptaken_by=None
            DefaultWork.objects.create(
                user=request.user,
                work=work,
                type="RevokedUptaken"
                )
            work.uptaken_is_read=False
        work.save()
        return Response({'message':'Work has been revoked successfully.'})
        
        