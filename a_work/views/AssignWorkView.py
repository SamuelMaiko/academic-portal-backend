from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_notifications.models import Notification
from a_userauth.models import CustomUser
from a_work.models import Work
from a_work.permissions import IsAdmin


class AssignWorkView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @swagger_auto_schema(
        operation_description="Assigns a work to a specific writer. Only admins can use this endpoint.",
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
                description='ID of the work to assign',
                required=True
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'writer': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the writer to whom the work will be assigned'
                )
            },
            required=['writer']
        ),
        responses={
            200: openapi.Response(
                description="Success",
                examples={
                    "application/json": {
                        "message": "Work has been assigned successfully."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": "Provide writer"
                    }
                }
            ),
            403: openapi.Response(
                description="Permission Denied",
                examples={
                    "application/json": {
                        "detail": "You do not have permission to perform this action."
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
        # adding a notification
        notification=Notification.objects.create(
            type="Assigned Work",
            message="work has been has been assigned",
            triggered_by=request.user,
            work=work
            )
        admins=get_admins()
        notification.users.add(*admins)
        notification.users.add(writer_to_assign)
        return Response({'message':'Work has been assigned successfully.'})
        
        