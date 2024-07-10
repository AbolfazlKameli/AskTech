import random

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Question, Answer, AnswerComment


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
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = '__all__'

    def get_comments(self, obj):
        comments = obj.comments.all()
        return AnswerCommentSerializer(comments, many=True).data


class AnswerCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    owner = serializers.StringRelatedField(read_only=True, required=False)
    answer = serializers.StringRelatedField(read_only=True, required=False)
    reply = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = AnswerComment
        fields = '__all__'

    def get_replies(self, obj):
        replies = obj.replies.all()
        return AnswerCommentSerializer(instance=replies, many=True).data

    def create(self, validated_data):
        request = self.context.get('request')
        answer_instance = get_object_or_404(Answer, id=request.query_params.get('answer_id'))
        AnswerComment.objects.create(
            owner=request.user,
            answer=answer_instance,
            body=validated_data['body'],
        )
