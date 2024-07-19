from django.utils import timezone
from rest_framework import serializers

from a_work.models import Work

from .SubmissionSerializer import SubmissionSerializer


class SubmittedWorkSerializer(serializers.ModelSerializer):
    submission=serializers.SerializerMethodField()

    class Meta:
        model=Work
        fields=['id','work_code','words', 'submission']

    def get_submission(self, obj):
        user=self.context["user"]
        # print(obj.submissions.filter(sender=user))
        return SubmissionSerializer(obj.submissions.filter(sender=user).first()).data