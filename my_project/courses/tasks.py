# courses/tasks.py
from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Course

@shared_task
def check_for_course_updates():
    """
    Задача для проверки обновлений курса.
    Проверяет, обновлялся ли курс в течение последних 4 часов.
    Если не обновлялся — отправляет уведомление.
    """
    four_hours_ago = timezone.now() - timedelta(hours=4)
    courses_to_notify = Course.objects.filter(updated_at__lt=four_hours_ago)

    for course in courses_to_notify:
        pass
