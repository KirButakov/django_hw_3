from django.db import models
from django.contrib.auth.models import User
from courses.models import Course, Lesson

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
    )

    user = models.ForeignKey(User, related_name='payments', on_delete=models.CASCADE)
    paid_course = models.ForeignKey(Course, related_name='payments', null=True, blank=True, on_delete=models.CASCADE)
    paid_lesson = models.ForeignKey(Lesson, related_name='payments', null=True, blank=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} for {self.paid_course or self.paid_lesson}"
