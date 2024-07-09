from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.QuestionListAPI.as_view(), name='home'),
    path('create_question/', views.QuestionCreateAPI.as_view(), name='question_create'),
    path('question/<slug:slug>/', views.QuestionDetailAPI.as_view(), name='question_detail'),
    path('question_update/<slug:slug>/', views.QuestionUpdateAPI.as_view(), name='question_update'),
    path('question_delete/<slug:slug>/', views.QuestionDestroyAPI.as_view(), name='question_delete'),
    path('create_answer/<slug:question_slug>/', views.AnswerCreateAPI.as_view(), name='answer_create'),
    path('answer_update/<int:answer_id>/', views.AnswerUpdateAPI.as_view(), name='answer_update'),
    path('answer_delete/<int:pk>/', views.AnswerDestroyAPI.as_view(), name='answer_delete'),
]
