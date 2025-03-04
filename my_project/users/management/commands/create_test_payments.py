from django.core.management.base import BaseCommand
from users.models import Payment
from django.contrib.auth.models import User
from courses.models import Course, Lesson

class Command(BaseCommand):
    help = 'Создание тестовых платежей'

    def handle(self, *args, **kwargs):
        user = User.objects.first()  # Получаем первого пользователя
        course = Course.objects.first()  # Получаем первый курс
        lesson = Lesson.objects.first()  # Получаем первый урок

        Payment.objects.create(
            user=user,
            paid_course=course,
            paid_lesson=None,
            amount=100.00,
            payment_method='cash'
        )

        Payment.objects.create(
            user=user,
            paid_course=None,
            paid_lesson=lesson,
            amount=50.00,
            payment_method='bank_transfer'
        )

        self.stdout.write(self.style.SUCCESS('Тестовые платежи созданы'))
