from django.urls import path
from rest_framework import routers

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeAPI.as_view(), name='home'),
]

router = routers.SimpleRouter()
router.register('question', views.QuestionViewSet)
urlpatterns += router.urls
