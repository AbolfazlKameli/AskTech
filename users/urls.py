from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UsersListAPI.as_view(), name='users_list')
]
