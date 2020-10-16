
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scarp_currency.settings')

app = Celery('scarp_currency')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

