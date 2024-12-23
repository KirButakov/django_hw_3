from rest_framework import serializers
from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class CourseWithLessonsSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'lesson_count', 'lessons']

    def get_lesson_count(self, obj):
        # Возвращаем количество уроков для курса
        return obj.lessons.count()
