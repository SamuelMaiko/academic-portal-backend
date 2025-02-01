from rest_framework import serializers
from a_work.models import Type  # Import your model

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ["id","name"] 
