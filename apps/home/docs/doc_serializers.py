from rest_framework import serializers


class DocAnswerAcceptSerializer(serializers.Serializer):
    message = serializers.CharField()


class DocDislikeSerializer(serializers.Serializer):
    message = serializers.CharField()
