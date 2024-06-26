from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UsersListAPI.as_view(), name='users_list'),
    path('register/', views.UserRegisterAPI.as_view(), name='user_register'),
    path('register/verify/<str:token>/', views.UserRegisterVerifyAPI.as_view(), name='user_register_verify'),
    path('register/resend_email/', views.ResendVerificationEmailAPI.as_view(), name='user_register_resend_email'),
    path('change_password/', views.ChangePasswordAPI.as_view(), name='change_password'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
