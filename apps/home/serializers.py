from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Question, Answer, AnswerComment, CommentReply, Tag


class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    tag = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Question
        exclude = ('slug',)


class ReplyCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    comment = serializers.StringRelatedField(read_only=True)
    reply = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        model = CommentReply
        fields = '__all__'

    @extend_schema_field(serializers.ListSerializer(child=serializers.DictField()))
    def get_replies(self, obj):
        replies = obj.i_replies.select_related('owner', 'comment', 'reply').all()
        return ReplyCommentSerializer(instance=replies, many=True).data


class AnswerCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    answer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AnswerComment
        fields = '__all__'

    @extend_schema_field(serializers.ListSerializer(child=ReplyCommentSerializer(many=True)))
    def get_replies(self, obj):
        replies = obj.replies.select_related('owner', 'comment', 'reply').filter(reply=None)
        return ReplyCommentSerializer(instance=replies, many=True).data


class AnswerSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    question = serializers.StringRelatedField(read_only=True)
    comments = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        exclude = ('accepted',)

    @extend_schema_field(serializers.ListSerializer(child=AnswerCommentSerializer(many=True)))
    def get_comments(self, obj):
        comments = obj.comments.all()
        return AnswerCommentSerializer(comments, many=True).data

    @extend_schema_field(serializers.IntegerField())
    def get_likes(self, obj):
        likes = obj.votes.select_related('owner', 'answer').filter(is_like=True)
        return likes.count()

    @extend_schema_field(serializers.IntegerField())
    def get_dislikes(self, obj):
        dislikes = obj.votes.select_related('owner', 'answer').filter(is_dislike=True)
        return dislikes.count()
