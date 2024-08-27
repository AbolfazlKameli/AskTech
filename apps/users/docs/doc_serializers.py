from rest_framework import serializers


class DocRegisterVerifySerializer(serializers.Serializer):
    message = serializers.CharField()
    token = serializers.CharField()
    refresh = serializers.CharField()


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class DocRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    message = serializers.CharField()
