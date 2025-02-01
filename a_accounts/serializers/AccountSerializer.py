from rest_framework import serializers

from a_userauth.models import CustomUser


class AccountSerializer(serializers.ModelSerializer):
    profile_picture_absolute = serializers.SerializerMethodField()

    class Meta: 
        model = CustomUser
        fields = ['id','registration_number','first_name','last_name','email','is_active','profile_picture_absolute']

    def get_profile_picture_absolute(self, obj):
        request = self.context.get('request')
        if obj.profile.profile_picture and request:
            return request.build_absolute_uri(obj.profile.profile_picture.url)
        return None
        
