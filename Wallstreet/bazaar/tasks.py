from __future__ import absolute_import, unicode_literals
from celery import task
from .models import *
from django.utils.crypto import get_random_string


# pip install eventlet
# install redis

# Run Redis Server  - "redis-server"
# Run Worker - "celery -A Wallstreet worker --pool=eventlet -l info"
# Run Scheduler Beat - "celery -A Wallstreet beat -l info"

# Add tasks in settings


@task()
def addNews():
    News.objects.create(title=get_random_string(10), description=get_random_string(50))
