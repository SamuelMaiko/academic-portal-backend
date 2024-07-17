from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.helpers import get_admins
from a_notifications.models import Notification
from a_work.models import Work
from a_work.permissions import IsAdmin
from a_work.serializers import CreateWorkSerializer


class CreateWorkView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, *args, **kwargs):
        self.check_object_permissions(request, request.user)
        serializer = CreateWorkSerializer(data=request.data)
        if serializer.is_valid():
            work=serializer.save(author=request.user)
            assigned_to=serializer.validated_data["assigned_to"]
            if assigned_to is not None:
                # adding a notification
                notification=Notification.objects.create(
                    type="Assigned Work",
                    message="work has been has been assigned",
                    triggered_by=request.user,
                    work=work
                    )
                admins=get_admins()
                notification.users.add(*admins)
                notification.users.add(assigned_to)
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
