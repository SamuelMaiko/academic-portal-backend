from rest_framework import serializers

from a_submissions.models import Submission


class AllSubmissionsSerializer(serializers.ModelSerializer):
    work=serializers.SerializerMethodField()  
    sender=serializers.SerializerMethodField() 
    claimed_by=serializers.SerializerMethodField() 
    claimed_by_me=serializers.SerializerMethodField() 

    class Meta:
        model=Submission
        fields=['id','message','file','sender', 'work','created_at','is_claimed','claimed_by',"claimed_by_me"]

    def get_claimed_by(self, obj):

        return {
            'id':obj.claimed_by.id if obj.claimed_by else None,
            'registration_number':obj.claimed_by.registration_number if obj.claimed_by else "",
            'first_name':obj.claimed_by.first_name if obj.claimed_by else "No one",
            'last_name':obj.claimed_by.last_name if obj.claimed_by else "at all."
            }
    def get_claimed_by_me(self, obj):
        request=self.context["request"]
        return obj.claimed_by==request.user if obj.claimed_by is not None else False

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