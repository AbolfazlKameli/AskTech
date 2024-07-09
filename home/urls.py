from django.urls import path
from rest_framework import routers

from . import views

app_name = 'home'
urlpatterns = [
    path('create_answer/<slug:question_slug>/', views.AnswerCreateAPI.as_view(), name='answer_create'),
    path('answer_update/<int:answer_id>/', views.AnswerUpdateAPI.as_view(), name='answer_update'),
    path('answer_delete/<int:pk>/', views.AnswerDestroyAPI.as_view(), name='answer_delete'),
]

router = routers.SimpleRouter()
router.register('question', views.QuestionViewSet)
urlpatterns += router.urls
