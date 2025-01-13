from django.test import TestCase
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson, Subscription

class CourseModelTests(TestCase):

    def setUp(self):
        # Получаем модель пользователя через get_user_model()
        User = get_user_model()

        # Очистим данные перед каждым тестом
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        Subscription.objects.all().delete()  # Очистка подписок

        # Создадим курс
        self.course = Course.objects.create(
            name="Test Course",  # Используем 'name', а не 'title'
            description="Test description",
            preview="test_preview_url"
        )

        # Создадим два урока
        self.lesson1 = Lesson.objects.create(
            course=self.course,
            name="Lesson 1",  # Используем 'name', а не 'title'
            description="Test lesson 1"
        )

        self.lesson2 = Lesson.objects.create(
            course=self.course,
            name="Lesson 2",  # Используем 'name', а не 'title'
            description="Test lesson 2"
        )

        # Создадим пользователя через get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

    def test_course_creation(self):
        # Проверяем, что курс был создан
        course = Course.objects.get(id=self.course.id)
        self.assertEqual(course.name, "Test Course")
        self.assertEqual(course.description, "Test description")
        self.assertEqual(course.preview, "test_preview_url")

    def test_lesson_creation(self):
        # Проверяем, что уроки были созданы и привязаны к курсу
        lesson1 = Lesson.objects.get(id=self.lesson1.id)
        lesson2 = Lesson.objects.get(id=self.lesson2.id)

        self.assertEqual(lesson1.name, "Lesson 1")
        self.assertEqual(lesson1.description, "Test lesson 1")
        self.assertEqual(lesson1.course, self.course)

        self.assertEqual(lesson2.name, "Lesson 2")
        self.assertEqual(lesson2.description, "Test lesson 2")
        self.assertEqual(lesson2.course, self.course)

    def test_subscription_creation(self):
        # Создаем подписку
        subscription = Subscription.objects.create(
            user=self.user,
            course=self.course
        )

        # Проверяем, что подписка была создана
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.course, self.course)

    def test_subscription_unique_together(self):
        # Проверяем, что уникальное сочетание user и course работает
        Subscription.objects.create(user=self.user, course=self.course)
        with self.assertRaises(Exception):
            Subscription.objects.create(user=self.user, course=self.course)

    def test_course_str(self):
        # Проверяем строковое представление курса
        self.assertEqual(str(self.course), "Test Course")

    def test_lesson_str(self):
        # Проверяем строковое представление урока
        self.assertEqual(str(self.lesson1), "Lesson 1")
        self.assertEqual(str(self.lesson2), "Lesson 2")

    def test_subscription_str(self):
        # Проверяем строковое представление подписки
        subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.assertEqual(str(subscription), f"{self.user} subscribed to {self.course.name}")
