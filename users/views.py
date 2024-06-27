from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from permissions import permissions
from utils import JWT_token, send_email
from . import serializers
from .models import User


class UsersListAPI(ListAPIView):
    """
    Returns list of users.\n
    allowed methods: GET.
    """
    permission_classes = [IsAdminUser, ]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserRegisterAPI(CreateAPIView):
    """
    Registers a User.\n
    allowed methods: POST.
    """
    model = User
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = [permissions.NotAuthenticated, ]


class UserRegisterVerifyAPI(APIView):
    """
    Verification view for registration.\n
    allowed methods: GET.
    """
    permission_classes = [permissions.NotAuthenticated, ]

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
    """
    makes a new token and send it with email.\n
    allowed methods: POST.
    """
    permission_classes = [permissions.NotAuthenticated, ]
    serializer_class = serializers.ResendVerificationEmailSerializer

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


class ChangePasswordAPI(APIView):
    """
    Changes a user password.\n
    allowed methods: POST.
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = serializers.ChangePasswordSerializer

    def put(self, request):
        srz_data = self.serializer_class(data=request.POST)
        if srz_data.is_valid():
            user = User.objects.get(id=self.request.user.id)
            old_password = srz_data.validated_data['old_password']
            new_password = srz_data.validated_data['new_password']
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Your password changed successfully!'}, status=status.HTTP_200_OK)
            return Response({'error': 'Your old password is not correct'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class SetPasswordAPI(APIView):
    """
    set user password for reset_password.\n
    allowed methods: POST.
    """
    permission_classes = [AllowAny, ]
    serializer_class = serializers.SetPasswordSerializer

    def post(self, request, token):
        srz_data = self.serializer_class(data=request.POST)
        user_id = JWT_token.decode_token(token)
        try:
            user = get_object_or_404(User, id=user_id)
        except Http404:
            return Response({'error': 'Activation link is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        except TypeError:
            return Response(user_id)
        if srz_data.is_valid():
            new_password = srz_data.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response({'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPI(APIView):
    """
    reset user passwrd.\n
    allowed methods: POST.
    """
    permission_classes = [AllowAny, ]
    serializer_class = serializers.ResetPasswordSerializer

    def post(self, request):
        srz_data = self.serializer_class(data=request.POST)
        if srz_data.is_valid():
            try:
                user = get_object_or_404(User, email=srz_data.validated_data['email'])
            except Http404:
                return Response({'error': 'user with this Email not found!'}, status=status.HTTP_400_BAD_REQUEST)

            token = JWT_token.generate_token(user)
            url = self.request.build_absolute_uri(
                reverse('users:set_password', kwargs={'token': token['token']})
            )
            send_email.send_link(user.email, url)
            return Response({'message': 'sent you a change password link!'}, status=status.HTTP_200_OK)
        return Response({'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class BlockTokenAPI(APIView):
    """
    blocks a deleted token\n
    allowed methods: POST.
    """
    serializer_class = serializers.TokenSerializer
    permission_classes = [IsAdminUser, ]

    def post(self, request):
        srz_data = self.serializer_class(data=request.POST)
        if srz_data.is_valid():
            token = RefreshToken(request.POST['refresh'])
            token.blacklist()
            return Response(data={'message': 'Token blocked successfully!'}, status=status.HTTP_200_OK)
        return Response(data={'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPI(RetrieveUpdateAPIView):
    """
    Retrieve or update user profile.\n
    allowed methods: GET, PUT, PATCH.\n
    GET: Retrieve, PUT: Full update, PATCH:partial update.
    """
    permission_classes = [permissions.IsOwnerOrReadOnly]
    serializer_class = serializers.UserProfileSerializer
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = User.objects.all()
