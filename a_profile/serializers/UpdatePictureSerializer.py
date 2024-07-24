from rest_framework import serializers
from a_profile.models import Profile

class UpdatePictureSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Profile    
        fields=['profile_picture']