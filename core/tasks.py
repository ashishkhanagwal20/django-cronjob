from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscription, EmailHistory
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.utils import timezone
import json
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def test_task(self):
    try:
        logger.info(f"Test task {self.request.id} started")
        # You can add more logic here if needed
        result = "Test task executed successfully!"
        logger.info(f"Test task {self.request.id} completed: {result}")
        return result
    except Exception as e:
        logger.error(f"Test task {self.request.id} failed: {str(e)}")
        raise  # Re-raise the exception to mark the task as failed


@shared_task
def send_newsletters():
    subscriptions = Subscription.objects.select_related("user", "topic").all()

    for subscription in subscriptions:
        subject = f"Newsletter Update: {subscription.topic.title}"
        message = f"""
        Hello {subscription.user.username},
        
        Here's your update for {subscription.topic.title}:
        {subscription.topic.description}
        
        Best regards,
        Newsletter Team
        """

        try:
            # Send email
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscription.user.email],
                fail_silently=False,
            )

            # Log the email
            EmailHistory.objects.create(
                user=subscription.user, subject=subject, content=message
            )
            logger.info(f"Newsletter sent to {subscription.user.email}")

        except Exception as e:
            logger.error(
                f"Error sending newsletter to {subscription.user.email}: {str(e)}"
            )

    return "Newsletters sent!"


def schedule_newsletter_task(sender, **kwargs):
    logger.info("Scheduling test task...")
    # Create an interval schedule (every 1 minute for testing)
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES,
    )

    # Create or update the periodic task
    PeriodicTask.objects.update_or_create(
        name="Test Task",
        defaults={
            "interval": schedule,
            "task": "core.tasks.test_task",  # Change to the test task
            "args": json.dumps([]),  # If you have arguments, pass them here
            "enabled": True,
            "start_time": timezone.now(),  # Start immediately
        },
    )
