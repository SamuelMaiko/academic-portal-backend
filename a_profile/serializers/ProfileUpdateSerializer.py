# serializers.py
from rest_framework import serializers

from a_profile.models import Profile


class ProfileUpdateSerializer(serializers.ModelSerializer):
    first_name=serializers.CharField(source='user.first_name')
    last_name=serializers.CharField(source='user.last_name')
    last_name=serializers.CharField(source='user.last_name')
    email=serializers.CharField(source='user.email')
    bio = serializers.CharField(required=False)
    bio_with_emojis=serializers.SerializerMethodField()
    

    class Meta:
        model=Profile
        fields=['bio','bio_with_emojis','first_name', 'last_name','phone_number', 'linkedin', 'country', 'county','email' ]
        
    def update(self, obj, validated_data):
        obj.bio=validated_data.get('bio', obj.bio)
        obj.country=validated_data.get('country', obj.country)
        obj.county=validated_data.get('county', obj.county)
        obj.phone_number=validated_data.get('phone_number', obj.phone_number)
        obj.linkedin=validated_data.get('linkedin', obj.linkedin)
        obj.save()

        if 'user' in validated_data:
            user_data=validated_data.pop('user',{})
            user=obj.user
            user.first_name=user_data.get('first_name', user.first_name)
            user.last_name=user_data.get('last_name', user.last_name)
            user.save()
        
        
        return obj
    
    def get_bio_with_emojis(self, obj):
        return obj.bio_with_emojis
    
        