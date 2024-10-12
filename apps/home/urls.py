from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeAPI.as_view(), name='home'),

    # Questions
    path('questions/<int:question_id>/answers/', views.CreateAnswerAPI.as_view(), name='answer-create'),

    # Answers
    path('answers/<int:answer_id>/like/', views.LikeAPI.as_view(), name='answer-like'),
    path('answers/<int:answer_id>/dislike/', views.DisLikeAPI.as_view(), name='answer-dislike'),
    path('answers/<int:answer_id>/accept/', views.AcceptAnswerAPI.as_view(), name='answer-accept'),

    # comments
    path('answers/<int:answer_id>/comments/', views.CreateCommentAPI.as_view(), name='comment-create'),

    # Replies
    path('comments/<int:comment_id>/replies/', views.CreateReplyAPI.as_view(), name='reply-create'),
    path('comments/<int:comment_id>/replies/<int:reply_id>/', views.CreateReplyAPI.as_view(), name='reply-create'),
]

router = DefaultRouter()
router.register('questions', views.QuestionViewSet)
router.register('answers', views.AnswerViewSet, basename='answer-viewset')
router.register('comments', views.CommentViewSet, basename='comments')
router.register('replies', views.ReplyViewSet, basename='reply')
urlpatterns += router.urls
