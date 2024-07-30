from rest_framework import serializers

from a_revisions.models import Revision


class EditRevisionSerializer(serializers.ModelSerializer):
    submit_before = serializers.DateTimeField(required=True)

    class Meta:
        model = Revision
        fields = ['id', 'submit_before']

    def update(self, instance, validated_data):
        instance.submit_before = validated_data.get('submit_before', instance.submit_before)
        instance.save()
        return instance
