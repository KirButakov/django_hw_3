from django.urls import path
from .views import (
    CourseListCreateView,
    CourseRetrieveUpdateDeleteView,
    LessonListCreateView,
    LessonRetrieveUpdateDeleteView,
    SubscriptionCreateView,
    SubscriptionDeleteView
)

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDeleteView.as_view(), name='course-retrieve-update-delete'),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDeleteView.as_view(), name='lesson-retrieve-update-delete'),
    path('subscriptions/', SubscriptionCreateView.as_view(), name='subscription-create'),
    path('subscriptions/<int:pk>/', SubscriptionDeleteView.as_view(), name='subscription-delete'),
]
