# serializers.py
from rest_framework import serializers

from a_profile.models import Profile


class ContactInfoSerializer(serializers.ModelSerializer):
    email=serializers.CharField(source='user.email')
    class Meta:
        model=Profile
        fields=['email','phone_number','linkedin']