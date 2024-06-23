import random

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.views import Response
from django.shortcuts import redirect

from utils import send_otp_code
from .models import User, OTPCode
from .serializers import UserSerializer, UserRegisterSerializer, OTPCodeSerializer


class UsersListAPI(ListAPIView):
    permission_classes = [IsAdminUser, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegisterAPI(APIView):
    http_method_names = ['post', 'options', 'head']
    serializer_class = UserRegisterSerializer

    def post(self, request):
        srz_data = UserRegisterSerializer(data=request.POST)
        if srz_data.is_valid():
            vd = srz_data.validated_data
            random_code = random.randint(10000, 99999)
            OTPCode.objects.create(email=vd['email'], otp=random_code)
            send_otp_code(vd['email'], random_code)
            request.session['registration_info'] = {
                'username': vd['username'],
                'email': vd['email'],
                'password': vd['password']
            }
            return redirect('users:user_register_verify')
        data = {'data': srz_data.data, 'errors': srz_data.errors, 'message': 'not registered!'}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterVerifyAPI(APIView):
    http_method_names = ['post', 'options', 'head']
    serializer_class = OTPCodeSerializer

    def post(self, request):
        user_session = request.session['registration_info']
        code_instance = OTPCode.objects.get(email__exact=user_session['email'])
        srz_data = OTPCodeSerializer(data=request.POST, partial=True)
        if srz_data.is_valid():
            vd = srz_data.validated_data
            if vd['otp'] == code_instance.otp:
                User.objects.create_user(username=user_session['username'], email=user_session['email'],
                                         password=user_session['password'])
                code_instance.delete()
                data = {'message': 'register successful', 'data': 'test'}
                return Response(data=data, status=status.HTTP_201_CREATED)
            data = {'errors': srz_data.errors}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

# TODO: fix bugs
