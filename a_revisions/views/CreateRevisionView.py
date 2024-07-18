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
            revision = serializer.save()

            # Creating notifications
            notification=Notification.objects.create(
                type="New Revision",
                message=f"A new revision has been created for",
                triggered_by=revision.reviewer,
                work=revision.work
            )
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
