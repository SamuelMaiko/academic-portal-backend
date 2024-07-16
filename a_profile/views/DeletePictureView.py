from rest_framework.views import APIView    
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from a_profile.serializers import UpdatePictureSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class DeletePictureView(APIView):
    permission_classes = [IsAuthenticated]
         
    def delete(self, request):
        profile=request.user.profile
        profile.profile_picture=None
        profile.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
            