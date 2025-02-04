from rest_framework import serializers

from a_revisions.models import Revision


class RevisionSerializer(serializers.ModelSerializer):
    work=serializers.SerializerMethodField()
    reviewer=serializers.SerializerMethodField()
    is_read=serializers.SerializerMethodField()
    writer=serializers.SerializerMethodField()

    class Meta:
        model = Revision
        fields = ['id', 'submit_before','work', 'status','reviewer','is_read','created_at','writer']

    def get_work(self, obj):
        return {
            'id':obj.work.id,
            'work_code':obj.work.work_code          
        }
    
    def get_reviewer(self, obj):
        return {
            'id':obj.reviewer.id,
            'registration_number':obj.reviewer.registration_number,
            'first_name':obj.reviewer.first_name,
            'last_name':obj.reviewer.last_name,
        }

    def get_is_read(self, obj):
        request=self.context["request"]
        return not obj.messages.exclude(sender=request.user).filter(is_read=False).exists()
    def get_writer(self, obj):
        return {
                "id":obj.work.writer.id if obj.work.writer else None,
                "first_name":obj.work.writer.first_name if obj.work.writer else None,
                "last_name":obj.work.writer.last_name if obj.work.writer else None
                }