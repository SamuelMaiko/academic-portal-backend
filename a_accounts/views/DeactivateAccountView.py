from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from a_accounts.signals import account_deactivated
from a_userauth.models import CustomUser
from a_work.permissions import IsAdmin


class DeactivateAccountView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(
        operation_description="Deactivate an existing account by ID and sends email to affected user.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the account to deactivate.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'reason': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Reason for account deactivation"
                ),
            },
            required=['reason']
        ),
        responses={
            200: openapi.Response(
                description="Account deactivated successfully",
                examples={
                    "application/json": {
                        "message": "Account deactivated successfully"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": "reason not provided."
                    }
                }
            ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": "Account matching query does not exist."
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
            401: openapi.Response(
                description="Unauthorized",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
        },
        tags=['Accounts']
    )

    
    def post(self, request,id):
        reason=request.data.get("reason")
        if not reason:
            return Response({'error':"reason not provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            account=CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response({'error':'account matching query does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, request.user)

        account.is_active = False
        account.save()
        
        # send email to inform user of deactivation
        account_deactivated.send(
            sender=None,
            user=account,
            reason=reason
        )

        return Response({'message': 'Account deactivated successfully'})