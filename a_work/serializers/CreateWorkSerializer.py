from rest_framework import serializers

from a_userauth.models import CustomUser  # Assuming your user model is named CustomUser
from a_work.models import Work


class CreateWorkSerializer(serializers.ModelSerializer):
    work_code=serializers.CharField(required=False)
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Work
        fields = ['id', 'deadline', 'work_code','words', 'type', 'assigned_to', 'comment','status']
        
    def update(self, instance, validated_data):
        print(validated_data)
        instance.deadline=validated_data.get('deadline', instance.deadline)
        instance.assigned_to=validated_data.get('assigned_to', instance.assigned_to)
        instance.words=validated_data.get('words', instance.words)
        instance.type=validated_data.get('type', instance.type)
        instance.comment=validated_data.get('comment', instance.comment)
        instance.status=validated_data.get('status', instance.status)
        instance.uptaken_by=None
        instance.save()
        return instance