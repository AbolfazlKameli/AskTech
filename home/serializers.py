from rest_framework import serializers

from .models import Question, Answer


class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = Question
        exclude = ('slug',)


class AnswerSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True, required=False)
    question = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = Answer
        fields = '__all__'
