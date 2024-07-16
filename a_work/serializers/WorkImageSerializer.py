from rest_framework import serializers
from a_work.models import WorkImage

class WorkImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=WorkImage
        fields=['id','image']