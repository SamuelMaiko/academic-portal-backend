from rest_framework import serializers

from a_preferences.models import Preference


class PreferenceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Preference
        fields=["id","dark_mode"]