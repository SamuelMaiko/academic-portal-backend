from a_profile.models import Profile
from rest_framework import serializers


class UpdatePictureSerializer(serializers.ModelSerializer):
    profile_picture=serializers.ImageField(required=True)
    profile_picture_absolute = serializers.SerializerMethodField()
    
    class Meta:
        model=Profile    
        fields=['profile_picture','profile_picture_absolute']
        
    def get_profile_picture_absolute(self, obj):
        request = self.context.get('request')
        if obj.profile_picture and request:
            return request.build_absolute_uri(obj.profile_picture.url)
        return None