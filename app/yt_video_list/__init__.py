from __future__ import absolute_import, unicode_literals

# This will make sure the celery is always imported when
# Django starts so that periodic_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
