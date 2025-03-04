from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def notify_subscribers_about_course_update(course_name, users_email):
    """
    Задача для отправки уведомлений подписчикам курса об обновлении.
    """
    send_mail(
        subject=f"Обновление курса {course_name}",
        message=f"Курс {course_name} был обновлен. Проверьте новые материалы!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=users_email,
    )
