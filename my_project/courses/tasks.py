from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Course, Lesson

@shared_task
def notify_subscribers_about_course_update():
    """
    Задача для проверки обновлений курсов.
    Проверяет, есть ли уроки, связанные с курсом, которые не обновлялись в течение последних 4 часов.
    Если такие уроки есть, отправляет уведомление администраторам.
    """
    four_hours_ago = timezone.now() - timedelta(hours=4)
    courses_to_notify = Course.objects.filter(
        lessons__updated_at__lt=four_hours_ago
    ).distinct()

    if courses_to_notify.exists():
        course_names = ", ".join([course.name for course in courses_to_notify])
        send_mail(
            subject="Обновление курсов",
            message=f"Следующие курсы имеют уроки, которые не обновлялись более 4 часов: {course_names}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['admin@example.com'],  # Замените на нужный адрес
        )
