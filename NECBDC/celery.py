import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NECBDC.settings')

app = Celery('NECBDC')
app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'check_payment': {
        'task': 'Exporter.tasks.check_payment',
        'schedule': 5.0,
    },
}

app.autodiscover_tasks()