from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from permissions import permissions
from utils import paginators
from . import serializers
from .models import Question, Answer, AnswerComment, CommentReply, Tag


class HomeAPI(APIView):
    """Home page."""
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[OpenApiParameter(name='tag', type=str, location=OpenApiParameter.QUERY, description='tag')])
    def get(self, request, *args, **kwargs):
        questions = Question.objects.all()
        if 'tag' in self.request.query_params:
            tag = get_object_or_404(Tag, slug=self.request.query_params['tag'])
            questions = tag.questions.all()
        srz_data = serializers.QuestionSerializer(questions, many=True)
        return Response(data={'message': 'this is home page', 'data': srz_data.data}, status=status.HTTP_200_OK)

    def options(self, request, *args, **kwargs):
        response = super().options(request, *args, **kwargs)
        response.headers['host'] = 'localhost'
        response.headers['user'] = request.user
        return response


class QuestionViewSet(ModelViewSet):
    """question CRUD operations ModelViewSet"""
    serializer_class = serializers.QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    pagination_class = paginators.StandardPageNumberPagination

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        return [permissions.IsOwnerOrReadOnly()]

    def create(self, request, *args, **kwargs):
        """creates a question object."""
        srz_data = self.get_serializer(data=self.request.POST)
        if srz_data.is_valid():
            slug = slugify(srz_data.validated_data['title'][:30])
            srz_data.save(slug=slug, owner=self.request.user)
            return Response(
                data={'data': srz_data.data, 'message': 'created successfully'},
                status=status.HTTP_201_CREATED
            )
        return Response(data={'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """shows detail of one question object."""
        question = self.get_object()
        srz_question = self.get_serializer(question)
        answers = question.answers.all()
        srz_answers = serializers.AnswerSerializer(answers, many=True)
        return Response(data={'question': srz_question.data, 'answers': srz_answers.data}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """updates one question object."""
        instance = self.get_object()
        srz_data = self.get_serializer(instance=instance, data=self.request.data, partial=True)
        if srz_data.is_valid():
            slug = slugify(srz_data.validated_data.get('title', instance.title)[:30])
            srz_data.save(slug=slug)
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """deletes an answer object."""
        return super().destroy(request, *args, **kwargs)


class AnswerViewSet(ModelViewSet):
    serializer_class = serializers.AnswerSerializer
    queryset = Answer.objects.all()
    http_method_names = ['post', 'put', 'patch', 'delete']

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [permissions.IsOwnerOrReadOnly()]

    @extend_schema(parameters=[
        OpenApiParameter(name='question_slug', type=str, location=OpenApiParameter.QUERY, description='question slug',
                         required=True)])
    def create(self, request, *args, **kwargs):
        """creates an answer object."""
        srz_data = self.get_serializer(data=self.request.POST)
        if srz_data.is_valid():
            question = get_object_or_404(Question, slug__exact=self.request.query_params['question_slug'])
            srz_data.save(question=question, owner=self.request.user)
            return Response(data={'message': 'created successfully'}, status=status.HTTP_201_CREATED)
        return Response(data={'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """updates an answer object."""
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """updates an answer object."""
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """deletes an answer object."""
        return super().destroy(request, *args, **kwargs)


class AnswerCommentViewSet(ModelViewSet):
    serializer_class = serializers.AnswerCommentSerializer
    queryset = AnswerComment.objects.all()
    http_method_names = ['post', 'put', 'patch', 'delete']

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [permissions.IsOwnerOrReadOnly()]

    def create(self, request, *args, **kwargs):
        srz_data = self.get_serializer(data=self.request.data)
        if srz_data.is_valid():
            answer = get_object_or_404(Answer, id=self.request.query_params['answer_id'])
            srz_data.save(owner=self.request.user, answer=answer)
            return Response(
                data={'message': 'created successfully'},
                status=status.HTTP_201_CREATED
            )
        return Response(data={'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class ReplyViewSet(ModelViewSet):
    serializer_class = serializers.ReplyCommentSerializer
    queryset = CommentReply.objects.all()
    http_method_names = ['post', 'put', 'patch', 'delete']

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [permissions.IsOwnerOrReadOnly()]

    @extend_schema(parameters=[
        OpenApiParameter(name='comment_id', type=int, location=OpenApiParameter.QUERY, description='comment_id',
                         required=True),
        OpenApiParameter(name='reply_id', type=int, location=OpenApiParameter.QUERY, description='reply_id')
    ])
    def create(self, request, *args, **kwargs):
        """created a reply object."""
        srz_data = self.get_serializer(data=self.request.data)
        if srz_data.is_valid():
            comment = get_object_or_404(AnswerComment, id=self.request.query_params.get('comment_id'))
            try:
                reply = CommentReply.objects.get(id=self.request.query_params.get('reply_id'))
            except CommentReply.DoesNotExist:
                reply = None
            srz_data.save(owner=self.request.user, comment=comment, reply=reply)
            return Response(data={'message': 'created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(data={'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)
