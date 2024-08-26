import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.django.settings')

app = Celery('forum')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.config_from_object('core.settings.celery_configs')
