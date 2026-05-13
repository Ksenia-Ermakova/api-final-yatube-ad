from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

# Импортируем для JWT (если не используем djoser)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Админка Django
    path('admin/', admin.site.urls),

    # API - подключаем все URL из приложения api
    # Все API-адреса будут начинаться с /api/v1/
    path('api/v1/', include('api.urls')),

    # Документация Redoc
    path('redoc/', TemplateView.as_view(template_name='redoc.html'), name='redoc'),

    # JWT эндпоинты (для получения и обновления токенов)
    # POST /api/v1/jwt/create/ - получить токен (отправить username и password)
    # POST /api/v1/jwt/refresh/ - обновить токен (отправить refresh токен)
    # POST /api/v1/jwt/verify/ - проверить токен (отправить access токен)
    path('api/v1/jwt/create/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/v1/jwt/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/v1/jwt/verify/', TokenVerifyView.as_view(),
         name='token_verify'),

    # Если используешь Djoser (раскомментировать после установки):
    # path('api/v1/auth/', include('djoser.urls')),
    # path('api/v1/auth/', include('djoser.urls.jwt')),
]
