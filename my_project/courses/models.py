from django.db import models


class Course(models.Model):
    """
    Модель для курсов.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Новое поле для цены
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/', blank=True, null=True)
    video_url = models.URLField()
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user} subscribed to {self.course.name}"

    def is_subscribed(self, user, course):
        return Subscription.objects.filter(user=user, course=course).exists()
