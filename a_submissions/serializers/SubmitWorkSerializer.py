from a_submissions.models import Submission
from a_work.models import Work
from rest_framework import serializers


class SubmitWorkSerializer(serializers.ModelSerializer):
    file=serializers.FileField(required=False, allow_null=True)
    message=serializers.CharField(required=False)
    
    class Meta:
        model=Submission
        fields=['id','message','file','sender', 'work']
