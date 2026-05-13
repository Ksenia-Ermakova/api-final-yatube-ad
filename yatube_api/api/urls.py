# Импортируем роутер из DRF
from .views import CommentViewSet
from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

# Импортируем наши ViewSet'ы
from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet

# Создаём роутер
# Роутер автоматически создаёт URL-адреса для ViewSet'ов
router = DefaultRouter()

# Регистрируем ViewSet'ы в роутере
# Первый аргумент - префикс URL (будет /posts/, /comments/ и т.д.)
# Второй аргумент - сам ViewSet
# Третий аргумент - имя для обратных ссылок
router.register(r'posts', PostViewSet, basename='post')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'follow', FollowViewSet, basename='follow')

# Для комментариев используем кастомный маршрут (через вложенный роутер)
# В DRF есть специальные инструменты, но проще добавить вручную в urlpatterns
# Вложенный URL: /posts/{post_id}/comments/

# URLs для комментариев будем обрабатывать отдельно

# Создаём список URL-адресов
urlpatterns = [
    # Подключаем все URL из роутера
    path('', include(router.urls)),

    # Вложенный маршрут для комментариев
    # re_path - регулярное выражение для сложных URL
    # (?P<post_id>\d+) - захватывает число как параметр post_id
    # comments/ - после этого идут стандартные действия
    re_path(r'^posts/(?P<post_id>\d+)/comments/$',
            CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
            name='comment-list'),

    re_path(r'^posts/(?P<post_id>\d+)/comments/(?P<pk>\d+)/$',
            CommentViewSet.as_view({'get': 'retrieve', 'put': 'update',
                                    'patch': 'partial_update', 'delete': 'destroy'}),
            name='comment-detail'),
]
