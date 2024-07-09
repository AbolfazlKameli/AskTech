from rest_framework import serializers

from .models import Question, Answer


# TODO: add relational fields
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ('slug',)
        extra_kwargs = {
            'owner': {'read_only': True, 'required': False}
        }


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        extra_kwargs = {
            'owner': {'read_only': True, 'required': False},
            'question': {'read_only': True, 'required': False}
        }
