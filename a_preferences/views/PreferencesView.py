from rest_framework.response import Response
from rest_framework.views import APIView

from a_preferences.serializers import PreferenceSerializer


class PreferencesView(APIView):
    def get(self, request):
        preferences=request.user.preferences
        serializer=PreferenceSerializer(preferences)
        return Response(serializer.data)