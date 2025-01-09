from rest_framework.pagination import PageNumberPagination

class CoursePagination(PageNumberPagination):
    page_size = 10  # Количество курсов на странице
    page_size_query_param = 'page_size'
    max_page_size = 100

class LessonPagination(PageNumberPagination):
    page_size = 5  # Количество уроков на странице
    page_size_query_param = 'page_size'
    max_page_size = 50
