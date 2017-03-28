from rest_framework import serializers


class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()
