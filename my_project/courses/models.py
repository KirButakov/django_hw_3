from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)  # Название курса
    preview = models.ImageField(upload_to='course_previews/', blank=True, null=True)  # Превью курса
    description = models.TextField()  # Описание курса

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=255)  # Название урока
    description = models.TextField()  # Описание урока
    preview = models.ImageField(upload_to='lesson_previews/', blank=True, null=True)  # Превью урока
    video_url = models.URLField()  # Ссылка на видео
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)  # Связь с курсом

    def __str__(self):
        return self.name
