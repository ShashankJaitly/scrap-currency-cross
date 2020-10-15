
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrap_currency.settings')

app = Celery('scrap_currency')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
