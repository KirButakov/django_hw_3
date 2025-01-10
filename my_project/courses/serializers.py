from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_video_url

class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_video_url])  # Валидатор применяется только к полю video_url

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseWithLessonsSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)  # Поле lessons только для чтения

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'lesson_count', 'lessons']

    def get_lesson_count(self, obj):
        # Возвращаем количество уроков для курса
        return obj.lessons.count()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['user', 'course']
