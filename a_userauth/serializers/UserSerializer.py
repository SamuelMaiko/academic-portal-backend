from rest_framework import serializers
from a_userauth.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CustomUser
        fields = ['registration_number','email',]
        
