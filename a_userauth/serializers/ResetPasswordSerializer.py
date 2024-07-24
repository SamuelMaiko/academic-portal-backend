from rest_framework import serializers

class ResetPasswordSerializer(serializers.Serializer):
    temp_token=serializers.UUIDField()
    new_password=serializers.CharField(write_only=True, min_length=8)
    