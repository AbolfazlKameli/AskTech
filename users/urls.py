from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = 'users'

token = [
    path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('block_token/', views.BlockTokenAPI.as_view(), name='token_block'),
]

urlpatterns = [
    path('', views.UsersListAPI.as_view(), name='users_list'),
    path('token/', include(token)),
    path('register/', views.UserRegisterAPI.as_view(), name='user_register'),
    path('register/verify/<str:token>/', views.UserRegisterVerifyAPI.as_view(), name='user_register_verify'),
    path('register/resend_email/', views.ResendVerificationEmailAPI.as_view(), name='user_register_resend_email'),
    path('change_password/', views.ChangePasswordAPI.as_view(), name='change_password'),
    path('set_password/<str:token>/', views.SetPasswordAPI.as_view(), name='set_password'),
]
