# tasks.py
import logging
from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from .models import CustomUser  # Make sure CustomUser is imported correctly

logger = logging.getLogger(__name__)

@shared_task
def delete_unverified_users():
    # Set a time threshold for deleting unverified users
    time_threshold = timezone.now() - timedelta(minutes=1)
    unverified_users = CustomUser.objects.filter(
        is_email_verified=False,
        otp_created_at__lt=time_threshold
    )
    
    # Delete and log the count of deleted unverified users
    deleted_count, _ = unverified_users.delete()
    
    if deleted_count > 0:
        logger.info(f"Deleted {deleted_count} unverified user(s).")
    else:
        logger.info("No unverified users to delete.")
    
    # Log how many unverified users matched the query
    logger.info(f"Unverified users found: {unverified_users.count()}")
