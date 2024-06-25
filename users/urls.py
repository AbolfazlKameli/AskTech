from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UsersListAPI.as_view(), name='users_list'),
    path('register/', views.UserRegisterAPI.as_view(), name='user_register'),
    path('register/verify/<str:token>/', views.UserRegisterVerifyAPI.as_view(), name='user_register_verify'),
    path('register/resend_email/', views.ResendVerificationEmailAPI.as_view(), name='user_register_resend_email'),
    path('login/', views.UserLoginAPI.as_view(), name='user_login'),
    path('login/verify/<str:token>/', views.UserLoginVerifyAPI.as_view(), name='user_login_verify'),
    path('logout/', views.UserLogoutAPI.as_view(), name='logout'),
    path('change_password/', views.ChangePasswordAPI.as_view(), name='change_password'),
]
