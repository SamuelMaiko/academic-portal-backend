from rest_framework import serializers

from a_work.models import DefaultWork


class DefaultWorkSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()
    work=serializers.SerializerMethodField()

    class Meta:
        model=DefaultWork
        fields=['id','type','user','work','created_at',]

    def get_user(self, obj):
        return {
            'id':obj.user.id,
            'registration_number':obj.user.registration_number,
            'first_name':obj.user.first_name,
            'last_name':obj.user.last_name 
            }
        
    def get_work(self, obj):
        return {
            'id':obj.work.id,
            'work_code':obj.work.work_code
            }
    