from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()

@shared_task
def block_inactive_users():
    """
    Задача для блокировки пользователей, которые не были активны более 30 дней.
    """
    thirty_days_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=thirty_days_ago, is_active=True)
    inactive_users.update(is_active=False)
