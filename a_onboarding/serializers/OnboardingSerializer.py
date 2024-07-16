from rest_framework import serializers
from a_userauth.models import CustomUser
from a_profile.models import Profile

class OnboardingSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100, source='profile.country')
    county = serializers.CharField(max_length=100, source='profile.county')
    phone_number = serializers.CharField(source='profile.phone_number')

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'country', 'county', 'phone_number']

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        # Update Profile related fields
        if 'profile' in validated_data:
            profile_data = validated_data.pop('profile', {})
            profile = instance.profile
            profile.phone_number = profile_data.get('phone_number', profile.phone_number)
            profile.country = profile_data.get('country', profile.country)
            profile.county = profile_data.get('county', profile.county)
            profile.save()

        return instance
