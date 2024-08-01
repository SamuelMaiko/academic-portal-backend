from django.urls import reverse
from rest_framework import serializers

from a_work.models import Work

from .WorkFileSerializer import WorkFileSerializer
from .WorkImageSerializer import WorkImageSerializer
from .WriterSerializer import WriterSerializer


class WorkDetailSerializer(serializers.ModelSerializer):
    is_bookmarked=serializers.SerializerMethodField()
    has_writer=serializers.SerializerMethodField()
    is_mine=serializers.SerializerMethodField()
    writer=serializers.SerializerMethodField()
    images=serializers.SerializerMethodField()
    files=serializers.SerializerMethodField()
    # files=WorkFileSerializer(many=True, read_only=True)
    images_zip_url = serializers.SerializerMethodField()
    
    
    class Meta:
        model=Work
        fields=['id','work_code','type','deadline','words','status','comment', 'created_at', 'is_bookmarked', 'has_writer','is_mine','images', 'files', 'writer','images_zip_url']

    def get_images(self, obj):
        request=self.context['request']
        return WorkImageSerializer(obj.images, many=True, context={'request':request}).data

    def get_files(self, obj):
        request=self.context['request']
        return WorkFileSerializer(obj.files, many=True, context={'request':request}).data
    
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
    
    def get_images_zip_url(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(reverse('download-all-images-zip', args=[obj.id]))