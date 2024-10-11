from django.urls import path
from .routers import NoListDefaultRouter

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeAPI.as_view(), name='home'),
    path('answer/like/<int:answer_id>/', views.LikeAPI.as_view(), name='answer-like'),
    path('answer/dislike/<int:answer_id>/', views.DisLikeAPI.as_view(), name='answer-dislike'),
    path('answer/accept/<int:answer_id>/', views.AcceptAnswerAPI.as_view(), name='answer-accept'),
    path('answer/create/<int:question_id>/', views.CreateAnswerAPI.as_view(), name='answer-create'),
    path('comment/create/<int:answer_id>/', views.CreateCommentAPI.as_view(), name='comment-create'),
    path('reply/create/<int:comment_id>/', views.CreateReplyAPI.as_view(), name='reply-create'),
    path('reply/create/<int:comment_id>/<int:reply_id>/', views.CreateReplyAPI.as_view(), name='reply-create'),
]

router = NoListDefaultRouter()
router.register('question', views.QuestionViewSet)
router.register('answer', views.AnswerViewSet, basename='answer-viewset')
router.register('comment', views.CommentViewSet, basename='comments')
router.register('reply', views.ReplyViewSet, basename='reply')
urlpatterns += router.urls
