import os
from celery import Celery
from decouple import config  # to load .env variables
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  # adjust 'core' to your project name

app = Celery('core')  # use your project name here

# Load broker URL and backend from .env via decouple
app.conf.broker_url = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
app.conf.result_backend = config('CELERY_RESULTS_BACKEND', default='redis://localhost:6379/0')

# Optional: other celery config from django settings, if you want to use CELERY_XXX settings there
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in all registered apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# For debugging
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
