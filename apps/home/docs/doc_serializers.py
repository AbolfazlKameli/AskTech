from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.home.models import Question, Tag
from apps.home.serializers import AnswerSerializer


class DocAnswerAcceptSerializer(serializers.Serializer):
    message = serializers.CharField()


class DocDislikeSerializer(serializers.Serializer):
    message = serializers.CharField()


class DocQuestionSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    tag = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all(), required=False)
    answers = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Question
        exclude = ('slug',)

    @extend_schema_field(serializers.ListSerializer(child=AnswerSerializer(many=True)))
    def get_answers(self, obj):
        answers = obj.answers.all()
        return AnswerSerializer(answers, many=True).data
