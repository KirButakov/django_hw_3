from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Course, Subscription


class CourseTests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.course = Course.objects.create(name="Test Course", description="Test Description", user=self.user)

    def test_create_course(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'New Course', 'description': 'New course description'}
        response = self.client.post('/courses/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)
        data = {'user': self.user.id, 'course': self.course.id}
        response = self.client.post('/subscriptions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unsubscribe_from_course(self):
        self.client.force_authenticate(user=self.user)
        subscription = Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.delete(f'/subscriptions/{subscription.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
