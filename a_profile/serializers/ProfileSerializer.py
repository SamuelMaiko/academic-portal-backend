# serializers.py
from rest_framework import serializers
from a_profile.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    registration_number=serializers.CharField(source='user.registration_number')
    first_name=serializers.CharField(source='user.first_name')
    last_name=serializers.CharField(source='user.last_name')

    class Meta:
        model=Profile
        fields=['profile_picture','bio','first_name', 'last_name','registration_number','county', ]