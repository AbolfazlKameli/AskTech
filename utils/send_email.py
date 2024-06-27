from django.conf import settings
from django.core.mail import send_mail


# TODO: send an HTML email body
def send_link(email, link):
    send_mail(
        subject="Verification",
        message=f'your verification code:\n{link}.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
