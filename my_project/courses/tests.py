from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Subscription

User = get_user_model()

class CourseAppTests(APITestCase):

    def setUp(self):
        # Создаем пользователей
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.moderator = User.objects.create_user(username="moderator", password="modpassword")
        self.moderator.groups.create(name="Moderators")

        # Создаем курс и урок
        self.course = Course.objects.create(name="Test Course", description="Test Description", user=self.user1)
        self.lesson = Lesson.objects.create(name="Test Lesson", description="Test Lesson Description", course=self.course, user=self.user1)

        # Создаем подписку
        self.subscription = Subscription.objects.create(user=self.user2, course=self.course)

    # Тесты CRUD для уроков
    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "name": "New Lesson",
            "description": "Lesson Description",
            "course": self.course.id
        }
        response = self.client.post("/lessons/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Lesson")

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.user1)
        data = {"name": "Updated Lesson Name"}
        response = self.client.patch(f"/lessons/{self.lesson.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Lesson Name")

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f"/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_retrieve_lesson(self):
        response = self.client.get(f"/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.lesson.name)

    # Тесты на подписку
    def test_create_subscription(self):
        self.client.force_authenticate(user=self.user1)
        data = {"course": self.course.id}
        response = self.client.post("/subscriptions/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(user=self.user1, course=self.course).exists())

    def test_delete_subscription(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f"/subscriptions/{self.subscription.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subscription.objects.filter(id=self.subscription.id).exists())

    def test_subscription_duplicate(self):
        self.client.force_authenticate(user=self.user2)
        data = {"course": self.course.id}
        response = self.client.post("/subscriptions/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Тесты на права доступа
    def test_lesson_access_denied(self):
        self.client.force_authenticate(user=self.user2)
        data = {"name": "Attempted Update"}
        response = self.client.patch(f"/lessons/{self.lesson.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_access_by_moderator(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(f"/courses/{self.course.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())

    def test_unauthenticated_access(self):
        response = self.client.get(f"/courses/{self.course.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
