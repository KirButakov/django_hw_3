from django.urls import path
from .views import LessonListCreateView, LessonRetrieveUpdateDeleteView, CourseListCreateView, \
    CourseRetrieveUpdateDeleteView

urlpatterns = [
    # Для работы с курсами
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDeleteView.as_view(), name='course-detail'),

    # Для работы с уроками
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDeleteView.as_view(), name='lesson-detail'),
]
