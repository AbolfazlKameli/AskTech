import jwt
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import MyTokenObtainPairSerializer


def generate_token(user, lifetime=None):
    token = MyTokenObtainPairSerializer.get_token(user, lifetime)
    return {"refresh": str(token), "token": str(token.access_token)}


def get_user(token):
    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        try:
            user = get_object_or_404(User, id=decoded_data['user_id'])
            return user
        except (Http404, TypeError):
            return Response(data={'error': 'Activation URL is invalid'}, status=status.HTTP_404_NOT_FOUND)
    except jwt.ExpiredSignatureError:
        return Response(data={'error': 'Activation link has expired!'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.InvalidTokenError:
        return Response(data={'error': 'Activation link is invalid!'}, status=status.HTTP_400_BAD_REQUEST)
