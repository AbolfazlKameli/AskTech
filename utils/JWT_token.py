from datetime import datetime, timedelta

import jwt
from django.conf import settings
from pytz import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.utils import datetime_to_epoch


class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token['email'] = user.email
        token['expire'] = datetime_to_epoch(datetime.now(tz=timezone('Asia/Tehran')) + timedelta(minutes=1))
        return token


def generate_token(user):
    refresh = CustomRefreshToken.for_user(user)
    return {"refresh": str(refresh), "token": str(refresh.access_token)}


def decode_token(token):
    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return decoded_data
    except jwt.ExpiredSignatureError:
        return {'error': 'Activation link has expired!'}
    except jwt.InvalidTokenError:
        return {'error': 'Activation link is invalid!'}
