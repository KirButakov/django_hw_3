from django.contrib.auth import get_user_model

class Course(models.Model):
    name = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='course_previews/', blank=True, null=True)
    description = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Добавление связи с пользователем

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/', blank=True, null=True)
    video_url = models.URLField()
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Добавление связи с пользователем

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'course')  # Уникальность подписки на курс для каждого пользователя

    def __str__(self):
        return f"{self.user} subscribed to {self.course.name}"

    def is_subscribed(self, user, course):
        return Subscription.objects.filter(user=user, course=course).exists()
