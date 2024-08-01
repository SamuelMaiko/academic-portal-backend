# serializers.py
from a_profile.models import Profile
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    registration_number=serializers.CharField(source='user.registration_number')
    first_name=serializers.CharField(source='user.first_name')
    last_name=serializers.CharField(source='user.last_name')
    role=serializers.CharField(source='user.role')
    profile_picture_absolute = serializers.SerializerMethodField()
    bio=serializers.SerializerMethodField()

    class Meta:
        model=Profile
        fields=['profile_picture','bio','first_name', 'last_name','role','registration_number','country','county','profile_picture_absolute' ]
        
    def get_profile_picture_absolute(self, obj):
        request = self.context.get('request')
        if obj.profile_picture and request:
            return request.build_absolute_uri(obj.profile_picture.url)
        return None
    
    def get_bio(self, obj):
        return obj.bio_with_emojis