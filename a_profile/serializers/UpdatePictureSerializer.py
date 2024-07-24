from rest_framework import serializers

from a_profile.models import Profile


class UpdatePictureSerializer(serializers.ModelSerializer):
    profile_picture=serializers.ImageField(required=True)
    
    class Meta:
        model=Profile    
        fields=['profile_picture']