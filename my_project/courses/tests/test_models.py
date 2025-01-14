from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson, Subscription

class CourseModelTests(APITestCase):
    def setUp(self):
        # Создание пользователя
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

        # Создание курса
        self.course = Course.objects.create(
            name="Test Course",
            description="Test description",
            preview="test_preview_url",
            user=self.user
        )

    def test_create_course(self):
        # Авторизация
        self.client.force_authenticate(user=self.user)

        # Данные для создания нового курса
        data = {
            "name": "New Course",
            "description": "New course description",
            "preview": "new_preview_url"
        }

        # Отправка POST-запроса для создания курса
        response = self.client.post("/api/courses/", data)

        # Проверка успешного создания курса
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Course")

    def test_create_lesson(self):
        # Авторизация
        self.client.force_authenticate(user=self.user)

        # Данные для создания нового урока
        data = {
            "name": "New Lesson",
            "description": "Lesson Description",
            "course": self.course.id,
            "video_url": "https://www.m.youtube.com/"
        }

        # Отправка POST-запроса для создания урока
        response = self.client.post("/api/lessons/", data)

        # Проверка успешного создания урока
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Lesson")
        self.assertEqual(response.data["course"], self.course.id)

class SubscriptionModelTests(APITestCase):
    def setUp(self):
        # Создание пользователя
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

        # Создание курса
        self.course = Course.objects.create(
            name="Test Course",
            description="Test description",
            preview="test_preview_url",
            user=self.user
        )

    def test_create_subscription(self):
        # Авторизация
        self.client.force_authenticate(user=self.user)

        # Данные для создания подписки
        data = {
            "user": self.user.id,
            "course": self.course.id
        }

        # Отправка POST-запроса для создания подписки
        response = self.client.post("/api/subscriptions/", data)

        # Проверка успешного создания подписки
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"], self.user.id)
        self.assertEqual(response.data["course"], self.course.id)

    def test_is_subscribed(self):
        # Создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        # Проверяем, что пользователь подписан на курс
        subscription = Subscription.objects.filter(user=self.user, course=self.course).exists()
        self.assertTrue(subscription)
