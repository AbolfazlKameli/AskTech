from django.core.mail import send_mail
from django.conf import settings


# TODO: send an HTML email body
def send_link(email, link):
    send_mail(
        "Verification",
        f'your verification code:\n{link}.',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
