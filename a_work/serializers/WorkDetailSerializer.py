from rest_framework import serializers
from a_work.models import Work
from .WorkImageSerializer import WorkImageSerializer
from .WorkFileSerializer import WorkFileSerializer
from .WriterSerializer import WriterSerializer

class WorkDetailSerializer(serializers.ModelSerializer):
    is_bookmarked=serializers.SerializerMethodField()
    has_writer=serializers.SerializerMethodField()
    is_mine=serializers.SerializerMethodField()
    writer=serializers.SerializerMethodField()
    images=WorkImageSerializer(many=True, read_only=True)
    files=WorkFileSerializer(many=True, read_only=True)
    
    
    class Meta:
        model=Work
        fields=['id','work_code','type','deadline','words','status','comment', 'created_at', 'is_bookmarked', 'has_writer','is_mine','images', 'files', 'writer']

    def get_is_bookmarked(self, obj):
        user=self.context['request'].user
        return user in obj.bookmarked_by.all()
    
    def get_has_writer(self, obj):
        return obj.has_writer

    def get_writer(self, obj):
        return WriterSerializer(obj.writer).data if obj.writer is not None else None

    def get_is_mine(self, obj):
        user=self.context['request'].user
        return obj.writer==user