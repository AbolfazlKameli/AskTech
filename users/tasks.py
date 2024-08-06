from celery import shared_task

from utils import send_email


@shared_task
def send_verification_email(url, email_address):
    send_email.send_link(email_address, url)
