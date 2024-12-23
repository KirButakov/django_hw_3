from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Payment
from courses.models import Course, Lesson

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'paid_course', 'paid_lesson', 'amount', 'payment_method', 'payment_date']

class UserProfileSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'payments']
