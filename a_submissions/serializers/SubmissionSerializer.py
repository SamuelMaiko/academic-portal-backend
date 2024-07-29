from a_submissions.models import Submission
from rest_framework import serializers


class SubmissionSerializer(serializers.ModelSerializer):
    work=serializers.SerializerMethodField()  
    sender=serializers.SerializerMethodField()
    claimed_by=serializers.SerializerMethodField()
      

    class Meta:
        model=Submission
        fields=['id','message','file','sender','claimed_by', 'work','created_at']

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

    def get_claimed_by(self, obj):
        return {
            'id':obj.claimed_by.id if obj.claimed_by else None,
            'registration_number':obj.claimed_by.registration_number if obj.claimed_by else None,
            'first_name':obj.claimed_by.first_name if obj.claimed_by else None,
            'last_name':obj.claimed_by.last_name if obj.claimed_by else None,
            'profile_picture':self.profile_picture_absolute(obj.claimed_by.profile) if obj.claimed_by else None
            }

    def profile_picture_absolute(self, obj):
        request = self.context.get('request')
        if obj.profile_picture and request:
            return request.build_absolute_uri(obj.profile_picture.url)
        return None