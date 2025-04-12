import os
from celery import Celery
from celery.signals import celeryd_after_setup
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = Celery("backend")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Configure the beat schedule
app.conf.beat_schedule = {
    "test-task-every-minute": {
        "task": "core.tasks.test_task",
        "schedule": 60.0,  # Every 60 seconds
    },
    "send-newsletters-daily": {
        "task": "core.tasks.send_newsletters",
        "schedule": 86400.0,  # Every 24 hours (in seconds)
    },
}


@app.task(bind=True)
def debug_task(self):
    logger.info(f"Request: {self.request!r}")


@celeryd_after_setup.connect
def setup_direct_queue(sender, instance, **kwargs):
    logger.info("Celery worker is ready!")
