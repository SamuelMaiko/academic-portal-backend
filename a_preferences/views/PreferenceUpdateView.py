from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from a_preferences.serializers import PreferenceSerializer


class PreferenceUpdateView(APIView):
    def put(self, request):
        preferences=request.user.preferences
        serializer=PreferenceSerializer(preferences, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)