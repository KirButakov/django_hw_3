from rest_framework import serializers
from .models import Course, Subscription, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_url', 'course']  # Поля модели Lesson


class CourseWithLessonsSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()  # Поле для количества уроков
    lessons = LessonSerializer(many=True, read_only=True)  # Связанные уроки
    is_subscribed = serializers.SerializerMethodField()  # Поле подписки

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'lesson_count', 'lessons', 'is_subscribed']

    def get_lesson_count(self, obj):
        # Возвращает количество уроков, связанных с курсом
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        # Проверяет, подписан ли пользователь на курс
        user = self.context.get('request').user  # Получение текущего пользователя
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False  # Если пользователь не авторизован
