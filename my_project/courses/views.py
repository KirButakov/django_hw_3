from rest_framework import generics
from .models import Course, Lesson, Subscription
from .serializers import CourseWithLessonsSerializer, LessonSerializer, SubscriptionSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrModerator  # Кастомное разрешение для проверки прав доступа

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseWithLessonsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]  # Доступ только для владельцев и модераторов

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Привязываем курс к текущему пользователю


class CourseRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseWithLessonsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]  # Доступ только для владельцев и модераторов

    def get_queryset(self):
        return Course.objects.filter(user=self.request.user)


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]  # Доступ только для владельцев и модераторов

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if course.user != self.request.user:
            raise PermissionDenied("You do not have permission to add lessons to this course.")
        serializer.save(user=self.request.user)  # Привязываем урок к текущему пользователю


class LessonRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]  # Доступ только для владельцев и модераторов

    def get_queryset(self):
        return Lesson.objects.filter(user=self.request.user)


class SubscriptionCreateView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SubscriptionDeleteView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
