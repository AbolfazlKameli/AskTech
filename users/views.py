from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.views import Response

from .models import User
from .serializers import UserSerializer, UserRegisterSerializer


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
            srz_data.create(srz_data.validated_data)
            data = {'data': srz_data.data, 'message': 'registered successfully',
                    'url': reverse('home:home', request=request)}
            return Response(data=data, status=status.HTTP_201_CREATED)
        data = {'data': srz_data.data, 'errors': srz_data.errors, 'message': 'not created'}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
