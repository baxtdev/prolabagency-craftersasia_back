# http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html - django redis
from __future__ import absolute_import, unicode_literals
import os

from django.utils.translation import gettext_lazy as _
from celery import Celery
from celery.schedules import crontab

from core.settings import CELERY_BROKER_URL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CORE')

app.conf.broker_url = CELERY_BROKER_URL

app.autodiscover_tasks()




app.conf.beat_schedule = {
    'add-every-6-secconds':{
        'task': 'chek_popular_items',
        'schedule': crontab(hour=18, minute=0), 
    }
}