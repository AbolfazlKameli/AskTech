from django.core.mail import send_mail
from django.conf import settings


def send_otp_code(email, random_code):
    send_mail(
        "Verification",
        f'your verification code:\n{random_code}.',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
