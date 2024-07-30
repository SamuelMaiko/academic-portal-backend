from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_notifications.models import Notification
from a_work.models import Work


class UptakeWorkView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""Enables a user to uptake work from the feed, notifies admins.
        NOTE: It removes the work from other user's bookmarks and notifies them too.""",
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
                description='ID of the work to uptake',
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Success",
                examples={
                    "application/json": {
                        "message": "Work has been uptaken successfully."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": "Work has already been allocated."
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
        
        if work.has_writer:
            return Response({'error':'Work has already been allocated.'}, status=status.HTTP_400_BAD_REQUEST)

        work.uptaken_by=request.user
        work.save()
        # adding a notification
        notification=Notification.objects.create(
            type="Uptaken Work",
            message="work has been has been uptaken",
            triggered_by=request.user,
            work=work
            )
        admins=get_admins()
        notification.users.add(*admins)
        
        # Get users who bookmarked the work, excluding the current user
        users=work.bookmarked_by.exclude(id=request.user.id)
        
        notifTwo=Notification.objects.create(
            type="System Notification",
            message="The work you bookmarked has been taken by another user",
            triggered_by=request.user,
            work=work,
            )
        notifTwo.users.add(*users)
        # Clear bookmarks
        work.bookmarked_by.clear()

        return Response({'message':'Work has been uptaken successfully.'})
        
        