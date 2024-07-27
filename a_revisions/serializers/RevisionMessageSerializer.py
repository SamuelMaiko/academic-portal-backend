from a_revisions.models import RevisionMessage
from rest_framework import serializers


class RevisionMessageSerializer(serializers.ModelSerializer):
    is_mine=serializers.SerializerMethodField()
    sender=serializers.SerializerMethodField()
    
    class Meta:
        model = RevisionMessage
        fields = ['id', 'message', 'file', 'image', 'is_read', 'sender', 'revision','is_mine', 'created_at']

    def get_is_mine(self, obj):
        user=self.context["request"].user
        return user==obj.sender
    
    def get_sender(self, obj):
        return {
            'id':obj.sender.id if obj.sender is not None else None ,
            'registration_number':obj.sender.registration_number if obj.sender is not None else None,
            'first_name':obj.sender.first_name if obj.sender is not None else None,
            'last_name':obj.sender.last_name if obj.sender is not None else None,
        }
    
    def create(self, validated_data):
        print(f"Validated data: {validated_data}")
        data={
            'message':validated_data.get('message'),
            'file':validated_data.get('file', None),
            'image':validated_data.get('image', None),  
            'revision':validated_data.get('revision', None),
            'sender':validated_data.get('sender', None),
            
        }
        revision_message=RevisionMessage.objects.create(**data)
        
        return revision_message
    
