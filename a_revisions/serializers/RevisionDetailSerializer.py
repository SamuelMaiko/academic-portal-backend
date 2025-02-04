from rest_framework import serializers

from a_revisions.models import Revision

from .RevisionMessageSerializer import RevisionMessageSerializer


class RevisionDetailSerializer(serializers.ModelSerializer):
    messages=serializers.SerializerMethodField()
    reviewer=serializers.SerializerMethodField()
    work=serializers.SerializerMethodField()
    
    class Meta:
        model = Revision
        fields = ['id', 'submit_before', 'status','reviewer','messages', 'work' ]

    def get_messages(self, obj):
        request=self.context['request']
        return RevisionMessageSerializer(obj.messages,many=True, read_only=True, context={'request':request}).data

    def get_reviewer(self, obj):
        return {
            'id':obj.reviewer.id,
            'registration_number':obj.reviewer.registration_number,
            'first_name':obj.reviewer.first_name,
            'last_name':obj.reviewer.last_name,
        }
    def get_work(self, obj):
        return {
            'id':obj.work.id if obj.work else None,
            'work_code':obj.work.work_code if obj.work else None,
        }
