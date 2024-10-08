from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from docs.serializers.doc_serializers import MessageSerializer
from permissions import permissions
from utils.update_response import update_response
from . import serializers
from .docs.doc_serializers import DocQuestionSerializer
from .models import Question, Answer, Comment, CommentReply, Vote


class HomeAPI(ListAPIView):
    """Home page."""
    permission_classes = [AllowAny]
    serializer_class = serializers.QuestionSerializer
    queryset = Question.objects.select_related('owner').all()
    filterset_fields = ['tag', 'owner', 'created']
    search_fields = ['title', 'body']


@extend_schema_view(
    create=extend_schema(
        responses={201: MessageSerializer}
    ),
    retrieve=extend_schema(
        responses={200: DocQuestionSerializer}
    ),
    update=extend_schema(
        responses={200: MessageSerializer}
    ),
    partial_update=extend_schema(
        responses={200: MessageSerializer}
    ),
)
class QuestionViewSet(ModelViewSet):
    """Question CRUD operations ModelViewSet."""
    serializer_class = serializers.QuestionSerializer
    queryset = Question.objects.select_related('owner').all()
    filterset_fields = ['tag', 'owner', 'created']
    search_fields = ['title', 'body']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        return [permissions.IsOwnerOrReadOnly()]

    def create(self, request, *args, **kwargs):
        """Creates a question object."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Automatically raise an exception if invalid
        serializer.save(owner=request.user)
        return Response(data={'message': 'Question created successfully.'}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """Shows detail of one question object."""
        response = super().retrieve(request, *args, **kwargs)
        answers = self.get_object().answers.all()
        srz_answers = serializers.AnswerSerializer(answers, many=True)
        response.data['answers'] = srz_answers.data
        return response

    def update(self, request, *args, **kwargs):
        """Updates one question object."""
        return update_response(
            super().update(request, *args, **kwargs),
            message='Question updated successfully.'
        )

    def partial_update(self, request, *args, **kwargs):
        """Updates a question object partially."""
        return update_response(
            super().partial_update(request, *args, **kwargs),
            message='Question updated successfully.'
        )

    def destroy(self, request, *args, **kwargs):
        """Deletes a question object."""
        return super().destroy(request, *args, **kwargs)


@extend_schema_view(
    update=extend_schema(responses={
        200: MessageSerializer
    }),
)
class AnswerViewSet(ModelViewSet):
    serializer_class = serializers.AnswerSerializer
    queryset = Answer.objects.select_related('owner', 'question').all()
    http_method_names = ['put', 'delete']
    permission_classes = [permissions.IsOwnerOrReadOnly]

    def update(self, request, *args, **kwargs):
        """updates an answer object."""
        return update_response(
            super().update(request, *args, **kwargs),
            'Answer Updated Successfully.'
        )

    def destroy(self, request, *args, **kwargs):
        """deletes an answer object."""
        return super().destroy(request, *args, **kwargs)


@extend_schema(
    responses={
        201: MessageSerializer
    }
)
class CreateAnswerAPI(CreateAPIView):
    """
    Creates Answers\n
    allowed methods:POST
    """
    serializer_class = serializers.AnswerSerializer
    queryset = Answer.objects.select_related('owner', 'question').all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        srz_data = self.get_serializer(data=self.request.data)
        if srz_data.is_valid():
            question = get_object_or_404(Question, id=kwargs.get('question_id'))
            srz_data.save(question=question, owner=self.request.user)
            return Response(data={'message': 'answer created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(data={'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    update=extend_schema(
        responses={200: MessageSerializer}
    ),
)
class CommentViewSet(ModelViewSet):
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.select_related('owner', 'answer').all()
    http_method_names = ['put', 'delete']
    permission_classes = [permissions.IsOwnerOrReadOnly]

    def update(self, request, *args, **kwargs):
        """updates a comment object."""
        return update_response(
            super().update(request, *args, **kwargs),
            'comment updated successfully.'
        )

    def destroy(self, request, *args, **kwargs):
        """deletes a comment object."""
        return super().destroy(request, *args, **kwargs)


@extend_schema(
    responses={
        201: MessageSerializer
    }
)
class CreateCommentAPI(CreateAPIView):
    """creates a comment object."""
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.select_related('owner', 'answer').all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """creates a comment object."""
        srz_data = self.get_serializer(data=self.request.data)
        if srz_data.is_valid():
            answer = get_object_or_404(Answer, id=kwargs.get('answer_id'))
            srz_data.save(owner=self.request.user, answer=answer)
            return Response(
                data={'message': 'comment created successfully.'},
                status=status.HTTP_201_CREATED
            )
        return Response(data={'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    update=extend_schema(
        responses={200: MessageSerializer}
    ),
)
class ReplyViewSet(ModelViewSet):
    serializer_class = serializers.ReplyCommentSerializer
    queryset = CommentReply.objects.select_related('owner', 'comment', 'reply').all()
    http_method_names = ['put', 'delete']
    permission_classes = [permissions.IsOwnerOrReadOnly]

    def update(self, request, *args, **kwargs):
        """updates a reply object."""
        return update_response(
            super().update(request, *args, **kwargs),
            'reply updated successfully.'
        )

    def destroy(self, request, *args, **kwargs):
        """destroys a reply object."""
        return super().destroy(request, *args, **kwargs)


@extend_schema(
    responses={
        201: MessageSerializer
    }
)
class CreateReplyAPI(CreateAPIView):
    """creates a reply object."""
    serializer_class = serializers.ReplyCommentSerializer
    queryset = CommentReply.objects.select_related('owner', 'comment', 'reply').all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """creates a reply object."""
        srz_data = self.get_serializer(data=self.request.data)
        if srz_data.is_valid():
            comment = get_object_or_404(Comment, id=kwargs.get('comment_id'))
            try:
                reply = CommentReply.objects.get(id=kwargs.get('reply_id'))
            except CommentReply.DoesNotExist:
                reply = None
            srz_data.save(owner=self.request.user, comment=comment, reply=reply)
            return Response(data={'message': 'reply created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(data={'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class LikeAPI(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: MessageSerializer})
    def get(self, request, answer_id):
        """add a like for each answer"""
        answer = get_object_or_404(Answer, id=answer_id)
        like = Vote.objects.filter(owner=self.request.user, answer=answer, is_like=True)
        dislike = Vote.objects.filter(owner=self.request.user, answer=answer, is_dislike=True)
        if like.exists():
            like.delete()
            return Response(data={'message': 'like removed.'}, status=status.HTTP_204_NO_CONTENT)
        if dislike.exists():
            dislike.delete()
        like.create(owner=self.request.user, answer=answer, is_like=True)
        return Response(data={'message': 'answer liked.'}, status=status.HTTP_200_OK)


class DisLikeAPI(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: MessageSerializer})
    def get(self, request, answer_id):
        """add a dislike for each answer"""
        answer = get_object_or_404(Answer, id=answer_id)
        dislike = Vote.objects.filter(owner=self.request.user, answer=answer, is_dislike=True)
        like = Vote.objects.filter(owner=self.request.user, answer=answer, is_like=True)
        if dislike.exists():
            dislike.delete()
            return Response(data={'message': 'dislike removed.'}, status=status.HTTP_200_OK)
        if like.exists():
            like.delete()
        dislike.create(owner=self.request.user, answer=answer, is_dislike=True)
        return Response(data={'message': 'answer disliked.'}, status=status.HTTP_200_OK)


class AcceptAnswerAPI(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: MessageSerializer})
    def get(self, request, answer_id):
        """accept an answer object"""
        answer = get_object_or_404(Answer, id=answer_id)
        if request.user.id == answer.question.owner.id:
            if not answer.accepted and not answer.question.has_accepted_answer():
                answer.accepted = True
                answer.owner.profile.score += 1
                answer.owner.profile.save()
                answer.save()
                return Response(data={'message': 'answer accepted.'}, status=status.HTTP_200_OK)
            return Response(
                data={'error': 'you can not accept an answer twice or accept two answers at the same time.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(data={'error': 'only question owner can perform this action.'},
                        status=status.HTTP_403_FORBIDDEN)
