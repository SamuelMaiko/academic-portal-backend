from rest_framework import serializers

from a_work.models import Work


class AssignedUptakenSerializer(serializers.ModelSerializer):
    # is_submitted=serializers.SerializerMethodField()
    # uptaken_is_read=serializers.SerializerMethodField()
    # assigned_is_read=serializers.SerializerMethodField()
    class Meta:
        model=Work
        fields=['id','work_code','deadline','words', 'type','status', 'is_submitted','uptaken_is_read','assigned_is_read']

    # def get_is_submitted(self, obj):
    #     pass
    
    # def get_assigned_is_read(self, obj):
    #     pass
    
    # def get_uptaken_is_read(self, obj):
    #     pass 