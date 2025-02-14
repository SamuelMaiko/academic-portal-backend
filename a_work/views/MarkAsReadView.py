from a_work.models import Work
from a_work.permissions import IsWorkWriter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class MarkAsReadView(APIView):
    permission_classes = [IsAuthenticated, IsWorkWriter]

    @swagger_auto_schema(
        operation_description="Marks work the user has been assigned or uptaken as read when they open it.",
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
                description='ID of the work to be marked as read',
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Work marked as read successfully",
                examples={
                    "application/json": {
                        "message": "Work marked as read."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": "Work matching query does not exist."
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
            403: openapi.Response(
                description="Forbidden",
                examples={
                    "application/json": {
                        "detail": "You do not have permission to perform this action."
                    }
                }
            )
        },
        tags=['Work']
    )

    def post(self, request, id):
        try:
            work= Work.objects.get(pk=id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, work)
        if not work.assigned_is_read:
            work.assigned_is_read=True
        if not work.uptaken_is_read:
            work.uptaken_is_read=True
        work.status="In Progress"
        work.save(update_fields=["assigned_is_read","uptaken_is_read","status"])
        
        return Response({'message':'Work marked as read.'})
        
        