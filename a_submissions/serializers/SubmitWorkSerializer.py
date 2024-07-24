from rest_framework import serializers

from a_submissions.models import Submission
from a_work.models import Work


class SubmitWorkSerializer(serializers.ModelSerializer):
    file=serializers.FileField(required=False, allow_null=True)
    
    class Meta:
        model=Submission
        fields=['id','message','file','sender', 'work']
