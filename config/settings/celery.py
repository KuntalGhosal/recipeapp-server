from __future__ import absolute_import,unicode_literals
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')

app = Celery('config.settings')

app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

#celery beat settings
app.conf.beat_schedule = {
    'send-mail-daily-at-3':{
        'task': 'recipe.scheduledtask.send_scheduled_mail_func',
        'schedule': crontab(hour=21, minute=5),
    }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'request: {self.request!r}')