from rest_framework import generics
from .models import Course, Lesson
from .serializers import CourseWithLessonsSerializer, LessonSerializer  # Импортируем новый сериализатор

# Для списка курсов и создания курса
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseWithLessonsSerializer  # Используем новый сериализатор для курсов с уроками

# Для получения, изменения и удаления конкретного курса
class CourseRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseWithLessonsSerializer  # Используем новый сериализатор для курсов с уроками

# Для списка уроков и создания урока
class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

# Для получения, изменения и удаления конкретного урока
class LessonRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
