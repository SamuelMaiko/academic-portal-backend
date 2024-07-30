from rest_framework import serializers

from a_preferences.models import Preference


class PreferenceSerializer(serializers.ModelSerializer):
    dark_mode=serializers.BooleanField(required=True)
    
    class Meta:
        model=Preference
        fields=["dark_mode"]