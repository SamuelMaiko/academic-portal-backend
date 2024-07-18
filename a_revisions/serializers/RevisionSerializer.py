from rest_framework import serializers

from a_revisions.models import Revision


class RevisionSerializer(serializers.ModelSerializer):
    work=serializers.SerializerMethodField()
    reviewer=serializers.SerializerMethodField()

    class Meta:
        model = Revision
        fields = ['id', 'submit_before','work', 'status','reviewer','created_at' ]

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
