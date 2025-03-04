from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Payment

# Сериализатор для создания пользователя
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'phone_number', 'city', 'avatar', 'date_of_birth', 'role']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number'),
            city=validated_data.get('city'),
            avatar=validated_data.get('avatar'),
            date_of_birth=validated_data.get('date_of_birth'),
            role=validated_data.get('role')
        )
        return user

# Добавление сериализатора для Payment
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

# Сериализатор для профиля пользователя
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'phone_number', 'city', 'avatar', 'date_of_birth', 'role']
