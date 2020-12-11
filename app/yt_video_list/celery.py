from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.utils.log import get_task_logger

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yt_video_list.settings')

app = Celery('yt_video_list')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

logger = get_task_logger(__name__)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        os.environ.get('FETCH_INTERVAL'),
        test.s(),
        name='Fetch videos from youtube periodically'
    )


@app.task()
def test(arg):
    logger.info(arg)
