from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import CustomUser
from django.utils import timezone
from datetime import timedelta

@receiver(post_save, sender= CustomUser)
def notify_admin_on_registration(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'New User Registration',
            f'A new user has registered: {instance.username}. Please review and approve the account.',
            'shenlyyamuyam25@gmail.com',
            ['shenlyyamuyam25@gmail.com'],
            fail_silently=False,
        )

