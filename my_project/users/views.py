from rest_framework import generics
from .models import Payment
from .serializers import PaymentSerializer, UserCreateSerializer, UserProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PaymentFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

# Список платежей с возможностью фильтрации
class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()  # Все платежи
    serializer_class = PaymentSerializer  # Сериализатор для платежей
    filter_backends = (DjangoFilterBackend,)  # Фильтрация по фильтрам
    filterset_class = PaymentFilter  # Фильтр для платежей

# Регистрация нового пользователя
class UserCreateView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()  # Получение модели пользователя
    serializer_class = UserCreateSerializer  # Сериализатор для регистрации
    permission_classes = [AllowAny]  # Открытый доступ для всех

# Получение пары токенов (access и refresh)
class ObtainTokenPairView(generics.GenericAPIView):
    permission_classes = [AllowAny]  # Открытый доступ для всех

    def post(self, request, *args, **kwargs):
        from rest_framework_simplejwt.views import TokenObtainPairView
        return TokenObtainPairView.as_view()(request, *args, **kwargs)

# Обновление токена
class RefreshTokenView(generics.GenericAPIView):
    permission_classes = [AllowAny]  # Открытый доступ для всех

    def post(self, request, *args, **kwargs):
        from rest_framework_simplejwt.views import TokenRefreshView
        return TokenRefreshView.as_view()(request, *args, **kwargs)

# Просмотр и обновление профиля пользователя
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()  # Получение модели пользователя
    serializer_class = UserProfileSerializer  # Сериализатор для профиля пользователя
    permission_classes = [IsAuthenticated]  # Требуется аутентификация для доступа
