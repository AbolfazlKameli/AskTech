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
from .models import Question, Answer


class HomeAPI(APIView):
    """Home page."""
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'message': 'this is home page'}, status=status.HTTP_200_OK)

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
        return Response({'question': srz_question.data, 'answers': srz_answers.data}, status=status.HTTP_200_OK)

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
    pagination_class = paginators.StandardPageNumberPagination
    http_method_names = ['post', 'put', 'patch', 'delete']

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated]
        return [permissions.IsOwnerOrReadOnly]

    @extend_schema(parameters=[
        OpenApiParameter(name='question_slug', type=str, location=OpenApiParameter.QUERY, description='question slug')])
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
