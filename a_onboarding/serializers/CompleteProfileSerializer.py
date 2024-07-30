from a_profile.models import Profile
from rest_framework import serializers


class CompleteProfileSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(allow_blank=True)
    profile_picture = serializers.ImageField(required=False)
    profile_picture_absolute = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture','profile_picture_absolute']

    def get_profile_picture_absolute(self, obj):
        request = self.context.get('request')
        if obj.profile_picture and request:
            return request.build_absolute_uri(obj.profile_picture.url)
        return None
