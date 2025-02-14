from rest_framework import serializers

from a_revisions.models import Revision


class EditRevisionSerializer(serializers.ModelSerializer):
    submit_before = serializers.DateTimeField(required=True)

    class Meta:
        model = Revision
        fields = ['id', 'submit_before','status']

    def update(self, instance, validated_data):
        instance.submit_before = validated_data.get('submit_before', instance.submit_before)
        instance.status = validated_data.get('status', instance.status)
        # print(instance.status)
        instance.save()
        return instance
