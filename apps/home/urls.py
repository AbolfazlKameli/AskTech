from django.urls import path
from rest_framework import routers

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeAPI.as_view(), name='home'),
    path('like/<int:answer_id>/', views.LikeAPI.as_view(), name='answer_like'),
    path('dislike/<int:answer_id>/', views.DisLikeAPI.as_view(), name='answer_dislike'),
    path('accept/<int:answer_id>/', views.AcceptAnswerAPI.as_view(), name='answer_accept'),
    path('answer/<int:question_id>/', views.CreateAnswerAPI.as_view(), name='answer_create'),
]

router = routers.DefaultRouter()
router.register('question', views.QuestionViewSet)
router.register('answers', views.AnswerViewSet, basename='answer-viewset')
router.register('answer_comments', views.AnswerCommentViewSet, basename='answer_comments')
router.register('reply', views.ReplyViewSet, basename='reply')
urlpatterns += router.urls
