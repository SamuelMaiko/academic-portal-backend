import os

from django.urls import reverse
from rest_framework import serializers

from a_work.models import WorkImage


class WorkImageSerializer(serializers.ModelSerializer):
    image_name = serializers.SerializerMethodField()
    image_extension = serializers.SerializerMethodField()
    combined = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
        
    class Meta:
        model=WorkImage
        fields=['id','image','image_name','image_extension','combined',"download_url"]

    def get_combined(self, obj):
        return os.path.splitext(os.path.basename(obj.image.name))[0]+"."+os.path.splitext(obj.image.name)[1].lstrip('.').lower()

    def get_image_name(self, obj):
        return os.path.splitext(os.path.basename(obj.image.name))[0]

    def get_image_extension(self, obj):
        return os.path.splitext(obj.image.name)[1].lstrip('.').lower()
    
    def get_download_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('download-work-image', args=[obj.id]))