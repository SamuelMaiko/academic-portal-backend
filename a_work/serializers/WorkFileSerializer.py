from rest_framework import serializers
from a_work.models import WorkFile
from pathlib import Path

class WorkFileSerializer(serializers.ModelSerializer):
    file_name=serializers.SerializerMethodField()
    
    class Meta:
        model=WorkFile
        fields=['id','file_name','file']

    def get_file_name(self, obj):
        name=Path(obj.file.name).name
        return name