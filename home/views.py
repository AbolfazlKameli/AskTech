from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

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
