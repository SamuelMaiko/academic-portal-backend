from rest_framework import serializers

from a_userauth.models import CustomUser


class AccountDetailSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source='profile.profile_picture', allow_null=True, required=False)
    bio = serializers.CharField(source='profile.bio', allow_blank=True, required=False)
    phone_number = serializers.CharField(source='profile.phone_number', allow_blank=True, required=False)
    country = serializers.CharField(source='profile.country', allow_blank=True, required=False)
    county = serializers.CharField(source='profile.county', allow_blank=True, required=False)    

    class Meta: 
        model = CustomUser
        fields = [
            'id',
            'profile_picture',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'country',
            'county',
            'registration_number',
            'role',
            'is_active',
            'date_joined',
            'last_login',
            'bio',
            ]
        extra_kwargs={
            'registration_number':{'required':False}
        }
        
    def update(self, instance, validated_data):
        instance.first_name=validated_data.get('first_name', instance.first_name)
        instance.last_name=validated_data.get('last_name', instance.last_name)
        instance.email=validated_data.get('email', instance.email)
        instance.role=validated_data.get('role', instance.role)
        instance.save()
        
        if 'profile' in validated_data:
            profile_data=validated_data.pop('profile', {})
            profile=instance.profile
            profile.profile_picture=profile_data.get('profile_picture', profile.profile_picture)
            profile.bio=profile_data.get('bio', profile.bio)
            profile.phone_number=profile_data.get('phone_number', profile.phone_number)
            profile.country=profile_data.get('country', profile.country)
            profile.county=profile_data.get('county', profile.county)
            profile.save()
        return instance
        