from rest_framework import serializers
from a_work.models import Work
from a_userauth.models import CustomUser  # Assuming your user model is named CustomUser

class CreateWorkSerializer(serializers.ModelSerializer):
    work_code=serializers.CharField(required=False)
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Work
        fields = ['id', 'deadline', 'work_code','words', 'type', 'assigned_to', 'comment']