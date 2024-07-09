from django.utils.text import slugify
from rest_framework import status
from rest_framework.generics import (CreateAPIView,
                                     UpdateAPIView,
                                     DestroyAPIView
                                     )
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from permissions import permissions
from utils import paginators
from . import serializers
from .models import Question, Answer


class QuestionViewSet(ModelViewSet):
    serializer_class = serializers.QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    pagination_class = paginators.StandardPageNumberPagination

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [permissions.IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
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
        question = self.get_object()
        srz_question = self.get_serializer(question)
        answers = question.answers.all()
        srz_answers = serializers.AnswerSerializer(answers, many=True)
        return Response({'question': srz_question.data, 'answers': srz_answers.data}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        srz_data = self.get_serializer(instance=instance, data=self.request.data, partial=True)
        if srz_data.is_valid():
            slug = slugify(srz_data.validated_data.get('title', instance.title)[:30])
            srz_data.save(slug=slug)
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerCreateAPI(CreateAPIView):
    """
    this view creates an answer.after answer create operation complete redirect user to question page.\n
    allowed methods: POST.
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = serializers.AnswerSerializer

    def create(self, request, *args, **kwargs):
        srz_data = self.serializer_class(data=self.request.POST)
        if srz_data.is_valid():
            question = Question.objects.get(slug__exact=kwargs['question_slug'])
            srz_data.save(question=question, owner=self.request.user)
            return Response(data={'message': 'created successfully'}, status=status.HTTP_201_CREATED)
        return Response(data={'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class AnswerUpdateAPI(UpdateAPIView):
    """
    this views updates an answer.\n
    allowed_methods: PUT, PATCH.
    """
    permission_classes = [permissions.IsOwnerOrReadOnly, ]
    queryset = Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    lookup_url_kwarg = 'answer_id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        srz_data = self.serializer_class(instance, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(data={'message': 'updated successfully'}, status=status.HTTP_200_OK)
        return Response(data={'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class AnswerDestroyAPI(DestroyAPIView):
    """
    this views deletes an answer.\n
    allowed_methods: DELETE.
    """
    permission_classes = [permissions.IsOwnerOrReadOnly, ]
    queryset = Answer.objects.all()
    serializer_class = serializers.QuestionSerializer
