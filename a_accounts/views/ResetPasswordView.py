from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.serializers import AccountSerializer
from a_accounts.signals import password_reset_signal
from a_userauth.models import CustomUser
from a_work.permissions import IsAdmin


class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def post(self, request, id):
        self.check_object_permissions(request, request.user)

        try:
            account=CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response({'error':'account matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        new_password=CustomUser.objects.make_random_password()
        account.set_password(new_password)
        account.save()
        
        # send email with new password
        password_reset_signal.send(
            sender=None, 
            user=account, 
            new_password=new_password, 
            )
        
        return Response({'message':f'Password changed successfully and sent to user.'})

        

        
        