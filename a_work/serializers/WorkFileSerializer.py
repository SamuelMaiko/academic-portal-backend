from pathlib import Path

from django.urls import reverse
from rest_framework import serializers

from a_work.models import WorkFile


class WorkFileSerializer(serializers.ModelSerializer):
    file_name=serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    
    class Meta:
        model=WorkFile
        fields=['id','file_name','file','download_url']

    def get_file_name(self, obj):
        name=Path(obj.file.name).name
        return name
    
    def get_download_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('download-work-file', args=[obj.id]))