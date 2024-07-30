from rest_framework import serializers

from a_userauth.models import CustomUser


class CreateAccountSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = CustomUser
        fields = ['id','registration_number','password','first_name','last_name','email','is_active',]
        extra_kwargs = {
            'password': {'write_only': True}, 
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'registration_number': {'required': False},
        }        
        
    def create(self, validated_data):
        new_user=CustomUser.objects.create(
            registration_number="wgf",
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            )
        new_user.set_password(validated_data.get('password'))
        new_user.save()
        return new_user
