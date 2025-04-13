from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscription, EmailHistory
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.utils import timezone
import json
import logging
import requests
from django.template.loader import render_to_string

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


def fetch_news_for_topic(topic):
    """Fetch news articles related to the topic"""
    try:
        api_key = settings.NEWS_API_KEY
        url = "https://newsapi.org/v2/everything"

        # Use get_search_query method which handles null search_query
        search_term = topic.get_search_query()

        params = {
            "q": search_term,
            "apiKey": api_key,
            "pageSize": 5,
            "language": "en",
            "sortBy": "publishedAt",  # Get latest news first
        }

        logger.info(f"Fetching news for topic: {topic.title} with query: {search_term}")
        response = requests.get(url, params=params)

        if response.status_code == 200:
            articles = response.json().get("articles", [])
            logger.info(f"Found {len(articles)} articles for topic: {topic.title}")
            return articles
        else:
            error_msg = response.json().get("message", "Unknown error")
            logger.error(f"NewsAPI error for {topic.title}: {error_msg}")
            return []
    except requests.RequestException as e:
        logger.error(f"Network error fetching news for {topic.title}: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching news for {topic.title}: {str(e)}")
        return []


@shared_task
def send_newsletters():
    subscriptions = Subscription.objects.select_related("user", "topic").all()

    for subscription in subscriptions:
        # Fetch fresh news for this topic
        articles = fetch_news_for_topic(subscription.topic)

        if not articles:
            logger.warning(f"No articles found for topic: {subscription.topic.title}")
            continue

        subject = f"Newsletter Update: {subscription.topic.title}"

        # Create article HTML separately
        article_html = ""
        for article in articles:
            article_html += f"""
            <div style="margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 20px;">
                <h4 style="color: #222; margin-bottom: 10px;">{article['title']}</h4>
                <p style="color: #666; margin-bottom: 15px;">{article['description']}</p>
                <a href="{article['url']}" style="color: #0066cc; text-decoration: none;">Read more -></a>
            </div>
            """

        # Create the complete HTML content
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #333;">Hello {subscription.user.username},</h2>
            <h3 style="color: #444;">Here are today's updates for {subscription.topic.title}:</h3>
            
            {'<p style="color: #666;">No news articles found for this topic today.</p>' if not articles else ''}
            
            {article_html}
            
            <p style="color: #666; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                Best regards,<br>Newsletter Team
            </p>
        </body>
        </html>
        """

        try:
            # Send email with HTML content
            send_mail(
                subject=subject,
                message="",  # Plain text version (empty as we're using HTML)
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscription.user.email],
                fail_silently=False,
                html_message=html_content,
            )

            # Log the email
            EmailHistory.objects.create(
                user=subscription.user, subject=subject, content=html_content
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
