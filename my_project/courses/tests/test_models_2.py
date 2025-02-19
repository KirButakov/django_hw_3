from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson
from django.urls import reverse


class LessonModelTests(APITestCase):
    def setUp(self):
        """
        Подготовка тестовых данных перед каждым тестом.
        """
        # Создание тестового пользователя
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="password123")

        # Создание курса (убираем preview, так как его нет в модели)
        self.course = Course.objects.create(
            name="Test Course",
            description="Test description",
            price=99.99,  # Добавляем price, так как в модели есть это поле
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
        """
        Тест просмотра урока.
        """
        # Авторизация пользователя
        self.client.force_authenticate(user=self.user)

        # Запрос GET на получение урока
        url = reverse('lesson-retrieve-update-delete', kwargs={'pk': self.lesson.id})
        response = self.client.get(url)

        # Проверяем успешный статус ответа и корректность данных
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Lesson")
        self.assertEqual(response.data['course'], self.course.id)

    def test_update_lesson(self):
        """
        Тест обновления урока.
        """
        self.client.force_authenticate(user=self.user)

        updated_data = {
            "name": "Updated Lesson",
            "description": "Updated description",
            "video_url": "https://www.youtube.com/updated_video",
            "course": self.course.id
        }

        url = reverse('lesson-retrieve-update-delete', kwargs={'pk': self.lesson.id})
        response = self.client.put(url, updated_data, format='json')

        # Проверяем статус ответа и корректность обновленных данных
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Lesson")
        self.assertEqual(response.data['description'], "Updated description")
        self.assertEqual(response.data['video_url'], "https://www.youtube.com/updated_video")

    def test_delete_lesson(self):
        """
        Тест удаления урока.
        """
        self.client.force_authenticate(user=self.user)

        url = reverse('lesson-retrieve-update-delete', kwargs={'pk': self.lesson.id})
        response = self.client.delete(url)

        # Проверяем статус ответа
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Убеждаемся, что урок действительно удалён
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())
