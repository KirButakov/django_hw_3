from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson
from django.urls import reverse

class LessonModelTests(APITestCase):
    def setUp(self):
        # Создание пользователя
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="password123")

        # Создание курса
        self.course = Course.objects.create(
            name="Test Course",
            description="Test description",
            preview="test_preview_url",
            user=self.user
        )

        # Создание урока
        self.lesson = Lesson.objects.create(
            name="Test Lesson",
            description="Test description",
            video_url="https://www.youtube.com/test_video",
            course=self.course,
            user=self.user
        )

    def test_view_lesson(self):
        # Авторизация
        self.client.force_authenticate(user=self.user)

        # Отправка GET-запроса для получения урока
        url = reverse('lesson-retrieve-update-delete', kwargs={'pk': self.lesson.id})
        response = self.client.get(url)

        # Проверка успешного получения урока
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Lesson")
        self.assertEqual(response.data['course'], self.course.id)

    def test_update_lesson(self):
        # Авторизация
        self.client.force_authenticate(user=self.user)

        # Данные для обновления урока
        updated_data = {
            "name": "Updated Lesson",
            "description": "Updated description",
            "video_url": "https://www.youtube.com/updated_video",
            "course": self.course.id
        }

        # Отправка PUT-запроса для обновления урока
        url = reverse('lesson-retrieve-update-delete', kwargs={'pk': self.lesson.id})
        response = self.client.put(url, updated_data)

        # Проверка успешного обновления урока
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Lesson")
        self.assertEqual(response.data['description'], "Updated description")
        self.assertEqual(response.data['video_url'], "https://www.youtube.com/updated_video")

    def test_delete_lesson(self):
        # Авторизация
        self.client.force_authenticate(user=self.user)

        # Отправка DELETE-запроса для удаления урока
        url = reverse('lesson-retrieve-update-delete', kwargs={'pk': self.lesson.id})
        response = self.client.delete(url)

        # Проверка успешного удаления урока
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Убедимся, что урок действительно удалён
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())
