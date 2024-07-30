from a_accounts.helpers import get_admins
from a_notifications.models import Notification
from a_submissions.models import Submission
from a_work.models import DefaultWork, Work
from a_work.permissions import IsAdmin
from a_work.serializers import CreateWorkSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class EditWorkView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin] 
    
    @swagger_auto_schema(
        operation_description="Edit an existing work entry.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'deadline': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Deadline for the work (ISO 8601 date-time format)'),
                'words': openapi.Schema(type=openapi.TYPE_INTEGER, description='Required number of words'),
                'type': openapi.Schema(type=openapi.TYPE_STRING, description='Type of the work'),
                'assigned_to': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID of the person assigned to this work'),
                'comment': openapi.Schema(type=openapi.TYPE_STRING, description='Additional comments or notes')
            },
            required=['deadline', 'words'],
        ),
        responses={
            200: openapi.Response(
                description="Work updated successfully",
                examples={
                    "application/json": {
                        "id": 1,
                        "deadline": "2024-07-17T15:00:00+03:00",
                        "work_code": "WK5201",
                        "words": 2500,
                        "type": "Reflection Paper",
                        "assigned_to": 1,
                        "comment": "Works"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": {
                        "error": "Invalid data"
                    }
                }
            ),
            404: openapi.Response(
                description="Not found",
                examples={
                    "application/json": {
                        "error": "Work matching query does not exist."
                    }
                }
            ),
        },
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True
                ),
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description='ID of the work to be edited.',
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        tags=['Work']
    )

    def put(self, request, id, format=None):
        try:
            work= Work.objects.get(pk=id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
        self.check_object_permissions(request, request.user)
        previous_writer=work.writer
        serializer = CreateWorkSerializer(work, data=request.data)
        if serializer.is_valid():
            work=serializer.save() 
            new_writer=work.writer
            if previous_writer!=new_writer:
                # Notifying the previous writer that their work has been assigned to another
                if previous_writer is not None:
                    # adding a notification
                    notification=Notification.objects.create(
                        type="ReAssigned Work",
                        message="work has been has been reassigned",
                        triggered_by=request.user,
                        work=work
                        )
                    admins=get_admins().exclude(id=request.user.id)
                    notification.users.add(*admins)
                    notification.users.add(previous_writer)

                # notifying the new writer of new work
                new_notification=Notification.objects.create(
                    type="Assigned Work",
                    message="work has been has been assigned",
                    triggered_by=request.user,
                    work=work
                    )
                new_notification.users.add(new_writer)
                
                # SET WORK to unread
                work.uptaken_is_read=False
                work.assigned_is_read=False
                work.is_submitted=False
                work.save()

                # ____________________________________________ handle users who bookmarked it
                # Get users who bookmarked the work, excluding the current user
                users=work.bookmarked_by.exclude(id=new_writer.id)
                
                notifTwo=Notification.objects.create(
                    type="System Notification",
                    message="The work you bookmarked has been taken by another user",
                    triggered_by=request.user,
                    work=work,
                    )
                notifTwo.users.add(*users)
                # Clear bookmarks
                work.bookmarked_by.clear()
                
            # updating default work records
            if previous_writer!=new_writer:
                submission=Submission.objects.filter(work=work, sender=previous_writer)
                if submission.exists():
                    DefaultWork.objects.create(
                        user=request.user,
                        work=work,
                        type="QualityIssues"
                        )
                    
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
