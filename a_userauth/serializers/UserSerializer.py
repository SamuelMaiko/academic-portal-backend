from a_userauth.models import CustomUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    profile_picture_absolute = serializers.SerializerMethodField()
    class Meta: 
        model = CustomUser
        fields = ['first_name','last_name','registration_number','email','profile_picture_absolute','role']
        
        
    def get_profile_picture_absolute(self, obj):
        request = self.context.get('request')
        if obj.profile.profile_picture and request:
            return request.build_absolute_uri(obj.profile.profile_picture.url)
        return None
        
