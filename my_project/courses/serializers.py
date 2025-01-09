from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_video_url
from .paginators import CoursePagination, LessonPagination

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [validate_video_url]  # Применение валидатора

class CourseWithLessonsSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)  # Добавлен аргумент read_only=True

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

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseWithLessonsSerializer
    pagination_class = CoursePagination  # Использование пагинатора для курсов

class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPagination  # Использование пагинатора для уроков
