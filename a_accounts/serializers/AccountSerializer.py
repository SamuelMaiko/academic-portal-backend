from rest_framework import serializers

from a_userauth.models import CustomUser


class AccountSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CustomUser
        fields = ['id','registration_number','first_name','last_name','email','is_active',]
        
