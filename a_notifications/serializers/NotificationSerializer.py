from rest_framework import serializers

from a_notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    triggered_by=serializers.SerializerMethodField()
    work=serializers.SerializerMethodField()
    is_read=serializers.SerializerMethodField()
    # is_read=serializers.BooleanField(source='notificationuser.is_read')

    class Meta:
        model=Notification
        fields=['id','message','type','triggered_by','is_read','work']
        
    def get_is_read(self, obj):
        user=self.context["request"].user
        return obj.notif_association.filter(user=user).first().is_read
    
    def get_triggered_by(self, obj):
        return {
            'id':obj.triggered_by.id,
            'registration_number':obj.triggered_by.registration_number,
            'first_name':obj.triggered_by.first_name,
            'last_name':obj.triggered_by.last_name,
            } if obj.triggered_by is not None else None

    def get_work(self, obj):
        return {
            'id':obj.work.id,
            'work_code':obj.work.work_code,
            'writer':{
                'id':obj.work.writer.id if obj.work.writer else None ,
                'registration_number':obj.work.writer.registration_number if obj.work.writer else None,
                'first_name':obj.work.writer.first_name if obj.work.writer else None,
                'last_name':obj.work.writer.last_name if obj.work.writer else None,
            }
            }