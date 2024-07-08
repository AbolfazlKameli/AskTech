from django.utils.text import slugify
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, UpdateAPIView, \
    RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from permissions import permissions
from utils import paginators
from . import serializers
from .models import Question


class QuestionListAPI(ListAPIView):
    """
    this view returns all questions.\n
    allowed methods: GET.
    """
    permission_classes = [AllowAny, ]
    queryset = Question.objects.all().order_by('-created')
    serializer_class = serializers.QuestionSerializer
    pagination_class = paginators.StandardPageNumberPagination
    lookup_field = 'slug'

    def options(self, request, *args, **kwargs):
        response = super().options(request, *args, **kwargs)
        response.headers['host'] = 'localhost'
        response.headers['user'] = request.user
        return response


class QuestionCreateAPI(CreateAPIView):
    """
    this view creates a question.
    allowed_methods: POST.
    """
    serializer_class = serializers.QuestionSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        srz_data = self.serializer_class(data=self.request.POST)
        if srz_data.is_valid():
            slug = slugify(srz_data.validated_data['title'][:30])
            srz_data.save(slug=slug, owner=self.request.user)
            return Response(
                data={'data': srz_data.data, 'message': 'created successfully'},
                status=status.HTTP_201_CREATED
            )
        return Response(data={'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailAPI(RetrieveAPIView):
    """
    this view can retrieve a question.\n
    allowed methods: GET.
    """
    permission_classes = [AllowAny, ]
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def retrieve(self, request, *args, **kwargs):
        question = self.get_object()
        srz_question = self.serializer_class(question)
        answers = question.answers.all().order_by('-created')
        srz_answers = serializers.AnswerSerializer(answers, many=True)
        return Response(data={'question': srz_question.data, 'answers': srz_answers.data}, status=status.HTTP_200_OK)


class QuestionUpdateAPI(UpdateAPIView):
    """
    this view can update a question.\n
    allowed methods: PUT, PATCH.
    """
    permission_classes = [permissions.IsOwnerOrReadOnly, ]
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        srz_data = self.serializer_class(instance, data=self.request.data, partial=True)
        if srz_data.is_valid():
            slug = slugify(srz_data.validated_data['title'][:30])
            srz_data.save(slug=slug)
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDestroyAPI(RetrieveUpdateDestroyAPIView):
    """
    this view can delete a question.\n
    allowed methods: DELETE.
    """
    permission_classes = [permissions.IsOwnerOrReadOnly, ]
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class AnswerCreateAPI(CreateAPIView):
    """
    this view creates an answer.\n
    allowed methods: POST.
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = serializers.AnswerSerializer

    def create(self, request, *args, **kwargs):
        srz_data = self.serializer_class(data=self.request.POST)
        if srz_data.is_valid():
            question = Question.objects.get(slug__exact=kwargs['slug'])
            srz_data.save(question=question, owner=self.request.user)
            return Response({'message': 'created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)
