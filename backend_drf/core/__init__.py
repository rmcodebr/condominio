from __future__ import absolute_import, unicode_literals

# Make celery app available as `celery_app`
from .celery import app as celery_app

__all__ = ('celery_app',)
