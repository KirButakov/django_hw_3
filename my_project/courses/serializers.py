from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_video_url  # Импорт валидатора для проверки ссылок


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(validators=[validate_video_url])  # Подключаем валидатор

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_url', 'course']


class CourseWithLessonsSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()  # Поле для количества уроков
    lessons = LessonSerializer(many=True, read_only=True)  # Связанные уроки
    is_subscribed = serializers.SerializerMethodField()  # Поле для проверки подписки

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'lesson_count', 'lessons', 'is_subscribed']

    def get_lesson_count(self, obj):
        """
        Возвращает количество уроков, связанных с курсом.
        """
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """
        Проверяет, подписан ли пользователь на курс.
        """
        request = self.context.get('request')  # Получаем объект запроса из контекста
        if request and request.user.is_authenticated:
            # Используем правильную обратную связь через subscription_set
            return obj.subscription_set.filter(user=request.user).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course']
