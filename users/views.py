from rest_framework import permissions
from rest_framework.generics import ListAPIView, CreateAPIView

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

    # def post(self, request, *args, **kwargs):
    #     srz_data = self.serializer_class(data=request.POST)
    #     if srz_data.is_valid():
    #         srz_data.create(srz_data.validated_data)
    #         data = {'data': srz_data.data}
    #         return Response(data)
    #     return Response(srz_data.errors)


class UserRegisterVerifyAPI(ListAPIView):
    ...
