from rest_framework import serializers


class DocRegisterVerifySerializer(serializers.Serializer):
    message = serializers.CharField()
    token = serializers.CharField()
    refresh = serializers.CharField()
