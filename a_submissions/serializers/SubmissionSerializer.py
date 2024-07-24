from rest_framework import serializers

from a_submissions.models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    work=serializers.SerializerMethodField()  
    sender=serializers.SerializerMethodField()  

    class Meta:
        model=Submission
        fields=['id','message','file','sender', 'work','created_at']

    def get_work(self, obj):
        return {
            'id':obj.work.id,
            'work_code':obj.work.work_code
            }
    
    def get_sender(self, obj):
        return {
            'id':obj.sender.id,
            'registration_number':obj.sender.registration_number,
            'first_name':obj.sender.first_name,
            'last_name':obj.sender.last_name 
            }