from django.urls import reverse
from rest_framework import serializers

from a_submissions.models import Submission
from a_work.models import Work


class SubmitWorkSerializer(serializers.ModelSerializer):
    file=serializers.FileField(required=False, allow_null=True)
    message=serializers.CharField(required=False)
    file_download_link=serializers.SerializerMethodField(required=False)      
    
    class Meta:
        model=Submission
        fields=['id','message','file','sender', 'work','file_download_link']

    def get_file_download_link(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(reverse('download-submission-file', args=[obj.id])) if obj.file else None
        return None