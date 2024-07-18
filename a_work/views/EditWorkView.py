from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_notifications.models import Notification
from a_work.models import Work
from a_work.permissions import IsAdmin
from a_work.serializers import CreateWorkSerializer


class EditWorkView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin] 

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
                # adding a notification
                notification=Notification.objects.create(
                    type="Assigned Work",
                    message="work has been has been reassigned",
                    triggered_by=request.user,
                    work=work
                    )
                admins=get_admins()
                notification.users.add(*admins)
                notification.users.add(previous_writer)

                # notification to new writer
                new_notification=Notification.objects.create(
                    type="Assigned Work",
                    message="work has been has been assigned",
                    triggered_by=request.user,
                    work=work
                    )
                new_notification.users.add(new_writer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
