from rest_framework import serializers
from a_work.models import Work

class WorkSerializer(serializers.ModelSerializer):
    is_bookmarked=serializers.SerializerMethodField()
    
    class Meta:
        model=Work
        fields=['id','work_code','deadline','words', 'type','created_at', 'is_bookmarked']

    def get_is_bookmarked(self, obj):
        user=self.context['request'].user
        return user in obj.bookmarked_by.all()