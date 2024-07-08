from datetime import datetime

import jwt
from django.conf import settings
from pytz import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.utils import datetime_to_epoch


class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user, lifetime=None):
        token = super().for_user(user)
        token['email'] = user.email
        if lifetime:
            token['expire'] = datetime_to_epoch(datetime.now(tz=timezone('Asia/Tehran')) + lifetime)
        return token


def generate_token(user, lifetime=None):
    refresh = CustomRefreshToken.for_user(user, lifetime)
    return {"refresh": str(refresh), "token": str(refresh.access_token)}


def decode_token(token):
    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        if 'expire' in decoded_data.keys() and datetime.now().timestamp() > decoded_data['expire']:
            return {'error': 'Activation link has expired!'}
        return decoded_data
    except jwt.ExpiredSignatureError:
        return {'error': 'Activation link has expired!'}
    except jwt.InvalidTokenError:
        return {'error': 'Activation link is invalid!'}
