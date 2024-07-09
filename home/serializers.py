import random

from rest_framework import serializers

from .models import Question, Answer


class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = Question
        exclude = ('slug',)

    def validate(self, attrs):
        question = Question.objects.filter(title=attrs.get('title'))
        if question.exists():
            attrs['title'] += str(random.randint(1, 10000))
        return attrs


class AnswerSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True, required=False)
    question = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = Answer
        fields = '__all__'
