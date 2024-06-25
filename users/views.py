from django.http import Http404
from django.urls import reverse

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import JWT_token, send_email
from .models import User
from .serializers import UserSerializer, UserRegisterSerializer, ResendVerificationEmailSerializer


class UsersListAPI(ListAPIView):
    """
    Returns list of users.\n
    allowed_method: GET.
    """
    permission_classes = [IsAdminUser, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegisterAPI(CreateAPIView):
    """
    Registers a User.\n
    allowed_method: POST.
    """
    model = User
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny, ]


class UserRegisterVerifyAPI(APIView):
    """
    Verification view for registration.\n
    allowed_method: GET.
    """

    def get(self, request, token):
        user_id = JWT_token.decode_token(token)
        try:
            user = get_object_or_404(User, pk=user_id)
            if user.is_active:
                return Response(data={'message': 'Your account already activated!'}, status=status.HTTP_400_BAD_REQUEST)
            user.is_active = True
            user.save()
            return Response(data={'message': 'Account activated successfully!'})
        except Http404:
            return Response({'message': 'Activation link is invalid!'}, status=status.HTTP_404_NOT_FOUND)
        except TypeError:
            return Response(user_id)


class ResendVerificationEmailAPI(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = ResendVerificationEmailSerializer

    def post(self, request):
        srz_data = self.serializer_class(data=request.POST)
        if srz_data.is_valid():
            user = srz_data.validated_data['user']
            token = JWT_token.generate_token(user)
            url = self.request.build_absolute_uri(
                reverse('users:user_register_verify', kwargs={'token': token['token']})
            )
            send_email.send_link(user.email, url)
            return Response(
                {"message: The activation email has been sent again successfully"},
                status=status.HTTP_200_OK,
            )
        return Response({'errors': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)
