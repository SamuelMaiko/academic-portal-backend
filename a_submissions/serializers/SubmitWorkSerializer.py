from rest_framework import serializers

from a_submissions.models import Submission


class SubmitWorkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Submission
        fields=['id','message','file','sender', 'work']
