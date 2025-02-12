from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.shortcuts import redirect

# Настройка для Swagger и ReDoc
schema_view = get_schema_view(
    openapi.Info(
        title="My Project API",
        default_version='v1',
        description="Документация для API проекта",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', lambda request: redirect('/swagger/')),
    # Основные маршруты API
    path('api/', include('courses.urls')),
    path('users/', include(('users.urls', 'users'), namespace='users')),

    # Добавляем аутентификацию через JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger и ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
