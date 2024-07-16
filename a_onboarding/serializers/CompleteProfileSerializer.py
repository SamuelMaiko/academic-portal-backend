from rest_framework import serializers
from a_profile.models import Profile

class CompleteProfileSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(allow_blank=True)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture',]
