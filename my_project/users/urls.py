from django.urls import path
from .views import UserCreateView, ObtainTokenPairView, RefreshTokenView, PaymentListView

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('register/', UserCreateView.as_view(), name='register'),  # Регистрация
    path('token/', ObtainTokenPairView.as_view(), name='token_obtain_pair'),  # Получение токена
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),  # Обновление токена
]
