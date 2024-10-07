from datetime import datetime

import jwt
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from pytz import timezone
from rest_framework import status
from rest_framework.response import Response

from apps.users.models import User


def generate_activation_token(user, lifetime=None):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.now(tz=timezone('Asia/Tehran')) + lifetime
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


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
