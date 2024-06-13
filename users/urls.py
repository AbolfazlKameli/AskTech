from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogOutView.as_view(), name='user_logout'),
]
