from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import JWT_token
from .models import User
from .serializers import UserSerializer, UserRegisterSerializer


class UsersListAPI(ListAPIView):
    permission_classes = [permissions.IsAdminUser, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegisterAPI(CreateAPIView):
    model = User
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserRegisterVerifyAPI(APIView):
    def get(self, request, token):
        user_id = JWT_token.decode_token(token)
        user = get_object_or_404(User, pk=user_id)
        if user.is_active:
            return Response(data={'message': 'Your account already activated!'}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        return Response(data={'message': 'Account activated successfully!'})
