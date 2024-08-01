from django.urls import reverse
from rest_framework import serializers

from a_revisions.models import RevisionMessage


class RevisionMessageSerializer(serializers.ModelSerializer):
    is_mine=serializers.SerializerMethodField()
    sender=serializers.SerializerMethodField()
    message=serializers.CharField(required=False)
    emoji_message=serializers.SerializerMethodField(required=False)
    image=serializers.ImageField(required=False)
    file=serializers.FileField(required=False)
    file_download_link=serializers.SerializerMethodField(required=False)
    image_download_link=serializers.SerializerMethodField(required=False)
    
    class Meta:
        model = RevisionMessage
        fields = ['id', 'message', 'file', 'image', 'is_read', 'sender', 'revision','is_mine', 'created_at','emoji_message','image_download_link','file_download_link']

    def get_is_mine(self, obj):
        user=self.context["request"].user
        return user==obj.sender
    
    def get_emoji_message(self, obj):
        return obj.message_with_emojis
    
    def get_sender(self, obj):
        return {
            'id':obj.sender.id if obj.sender is not None else None ,
            'registration_number':obj.sender.registration_number if obj.sender is not None else None,
            'first_name':obj.sender.first_name if obj.sender is not None else None,
            'last_name':obj.sender.last_name if obj.sender is not None else None,
        }
    
    def create(self, validated_data):
        # print(f"Validated data: {validated_data}")
        data={
            'message':validated_data.get('message'),
            'file':validated_data.get('file', None),
            'image':validated_data.get('image', None),  
            'revision':validated_data.get('revision', None),
            'sender':validated_data.get('sender', None),
            
        }
        revision_message=RevisionMessage.objects.create(**data)
        
        return revision_message
    
    def get_image_download_link(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(reverse('download-message-image', args=[obj.id])) if obj.image else None
    
    def get_file_download_link(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(reverse('download-message-file', args=[obj.id])) if obj.file else None
