from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_notifications.models import Notification
from a_revisions.models import Revision
from a_revisions.serializers import CreateRevisionSerializer
from a_work.models import Work
from a_work.permissions import IsAdmin


class CreateRevisionView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @swagger_auto_schema(
        operation_description="Create a new revision for a specific work.",
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
                description='ID of the work to create a revision for',
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['submit_before'],
            properties={
                'submit_before': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Deadline for the revision')
            }
        ),
        responses={
            201: openapi.Response(
                description="Revision created successfully",
                examples={
                    "application/json": {
                        "id": 5,
                        "work": 8,
                        "reviewer": 3,
                        "submit_before": "2024-07-25T15:00:00+03:00",
                        "status": "Not started",
                        "opened_by_reviewer": True,
                        "opened_by_writer": False
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "submit_before": [
                            "This field is required."
                        ]
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

    
    def post(self, request,id):
        self.check_object_permissions(request, request.user)

        try:
            work= Work.objects.get(pk=id)
        except Work.DoesNotExist:
            return Response({'error':'work matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        data=request.data.copy()
        data["reviewer"]=request.user.id
        data["work"]=work.id
        serializer = CreateRevisionSerializer(data=data)
        if serializer.is_valid():
            revision = serializer.save(reviewer=request.user)

            # Creating notifications
            notification=Notification.objects.create(
                type="New Revision",
                message=f"A new revision has been created for",
                triggered_by=revision.reviewer,
                work=revision.work
            )
            
            if revision.work.writer:
                notification.users.add(revision.work.writer)

            # Notify admins
            admins = get_admins()
            new_notification=Notification.objects.create(
                type="System Notification",
                message=f"A new revision has been created for ",
                triggered_by=revision.reviewer,
                work=revision.work
            )
            new_notification.users.add(*admins)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
