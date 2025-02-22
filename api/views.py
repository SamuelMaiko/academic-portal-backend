from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from a_userauth.models import CustomUser

class FirstUserRegistrationNumber(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        first_user = CustomUser.objects.first()
        if first_user:
            return Response({"registration_number": first_user.registration_number})
        else:
            return Response({"error": "No users found"})

