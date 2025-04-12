from django.apps import AppConfig
from django.db.models.signals import post_migrate
import logging

logger = logging.getLogger(__name__)


class CoreConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = "core"

    def ready(self):
        logger.info("Core app is ready, connecting post_migrate signal.")
        from .tasks import schedule_newsletter_task

        post_migrate.connect(schedule_newsletter_task, sender=self)
