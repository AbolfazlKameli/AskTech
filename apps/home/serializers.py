from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Question, Answer, Comment, CommentReply, Tag


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


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    answer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
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

    @extend_schema_field(serializers.ListSerializer(child=CommentSerializer(many=True)))
    def get_comments(self, obj):
        comments = obj.comments.all()
        return CommentSerializer(comments, many=True).data

    @extend_schema_field(serializers.IntegerField())
    def get_likes(self, obj):
        return self.get_votes_count(obj, is_like=True)

    @extend_schema_field(serializers.IntegerField())
    def get_dislikes(self, obj):
        return self.get_votes_count(obj, is_dislike=True)

    def get_votes_count(self, obj, is_like=None, is_dislike=None):
        votes = obj.votes.select_related('owner', 'answer')
        if is_like is not None:
            votes = votes.filter(is_like=is_like)
        if is_dislike is not None:
            votes = votes.filter(is_dislike=is_dislike)
        return votes.count()
