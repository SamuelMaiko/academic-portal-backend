from rest_framework import serializers

from a_revisions.models import Revision


class CreateRevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = ['id','work', 'reviewer', 'submit_before','status', 'opened_by_reviewer', 'opened_by_writer']
