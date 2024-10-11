from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.urls import reverse

from apps.users.models import User
from utils import JWT_token, send_email


@shared_task
def send_verification_email(email_address: str, user_id: int, action: str, message: str):
    user = User.objects.get(id=user_id)
    token = JWT_token.generate_activation_token(user, timedelta(minutes=1))
    url = f"http://{settings.DOMAIN}{reverse('users:user-register-verify', args=[token])}"
    if action == 'reset_password':
        url = f"http://{settings.DOMAIN}{reverse('users:set-password', args=[token])}"
    send_email.send_link(email_address, url, message)
