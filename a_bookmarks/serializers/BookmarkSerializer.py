from rest_framework import serializers
from a_work.models import Work
from a_bookmarks.models import Bookmark

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'work']
        read_only_fields = ['id']
