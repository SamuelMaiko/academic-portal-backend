from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.signals import account_activated
from a_userauth.models import CustomUser
from a_work.permissions import IsAdmin


class ActivateAccountView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def post(self, request,id):
        try:
            account=CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response({'error':'account matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, request.user)

        account.is_active = True
        account.save()
        
        # send email to inform user of deactivation
        account_activated.send(
            sender=None,
            user=account,
        )

        return Response({'message': 'Account activated successfully'})