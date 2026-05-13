"""
Вьюсеты (контроллеры) для API Yatube.
Обрабатывают запросы и возвращают ответы.
"""

# Импортируем классы из DRF
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter

# Импортируем модели
from posts.models import Post, Comment, Group, Follow

# Импортируем сериализаторы
from .serializers import PostSerializer, CommentSerializer, \
    GroupSerializer, FollowSerializer

# Импортируем разрешения
from .permissions import IsAuthorOrReadOnly, IsAuthenticatedForFollow, \
    IsAuthenticatedOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для постов.
    ModelViewSet даёт все CRUD операции: GET, POST, PUT, PATCH, DELETE.
    """

    # Берём все посты из базы данных
    queryset = Post.objects.all()

    # Какой сериализатор использовать
    serializer_class = PostSerializer

    # Какие разрешения применять
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        """
        При создании поста автоматически подставляем автора.
        """
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для комментариев.
    """

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        """
        Возвращаем только комментарии к конкретному посту.
        post_id передаётся в URL.
        """
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        """
        При создании комментария привязываем его к посту и автору.
        """
        post_id = self.kwargs.get('post_id')
        serializer.save(
            author=self.request.user,
            post_id=post_id
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для сообществ.
    ReadOnlyModelViewSet даёт только GET запросы (только чтение).
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # Отключаем пагинацию для групп, чтобы возвращался список, а не словарь
    pagination_class = None


class FollowViewSet(
    mixins.CreateModelMixin,   # Добавляет метод POST (создание)
    mixins.ListModelMixin,     # Добавляет метод GET (список)
    viewsets.GenericViewSet    # Базовая функциональность
):
    """
    Вьюсет для подписок.
    Только два метода: GET /follow/ (список подписок)
    и POST /follow/ (создать подписку).
    """

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticatedForFollow,)

    # Настройки поиска (параметр ?search=username)
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    # Отключаем пагинацию для подписок, чтобы возвращался список, а не словарь
    pagination_class = None

    def get_queryset(self):
        """
        Возвращаем только подписки текущего пользователя.
        """
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        При создании подписки подставляем текущего пользователя.
        """
        serializer.save(user=self.request.user)
