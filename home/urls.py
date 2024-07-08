from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.QuestionListAPI.as_view(), name='home'),
    path('create_question/', views.QuestionCreateAPI.as_view(), name='question_create'),
    path('questions/<slug:slug>/', views.QuestionDetailUpdateDestroyAPI.as_view(), name='question_RUD'),
    path('answer/<slug:slug>/', views.AnswerCreateAPI.as_view(), name='answer_create'),
]
