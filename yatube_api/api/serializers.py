"""
Сериализаторы для API Yatube.
Сериализаторы преобразуют данные из базы данных в JSON и обратно.
"""

# Импортируем нужные классы из Django REST Framework
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

# Импортируем модели из приложения posts
from posts.models import Comment, Post, Follow, Group

# Импортируем модель пользователя (встроенная в Django)
from django.contrib.auth import get_user_model

# Получаем модель пользователя
User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для постов (модель Post).
    Превращает пост в JSON и обратно.
    """

    # Поле author: выводит username автора, а не его ID
    # read_only=True - это поле только для чтения, изменить через API нельзя
    # slug_field='username' - используем поле username как значение
    author = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        # Указываем, для какой модели этот сериализатор
        model = Post

        # fields = '__all__' означает: использовать ВСЕ поля модели Post
        # Это включает: id, text, pub_date, author, image, group
        fields = '__all__'

        # Эти поля будут только для чтения (их нельзя изменить через API)
        read_only_fields = ('id', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комментариев (модель Comment).
    """

    # Автор комментария - только для чтения, выводим username
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'

        # Поле post нельзя редактировать через API,
        # оно будет автоматически подставляться из URL
        read_only_fields = ('id', 'created', 'post')


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для сообществ (модель Group).
    """

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для подписок (модель Follow).
    """

    # Поле user - кто подписывается
    # read_only=True - это поле только для чтения
    # CurrentUserDefault() - автоматически подставляет текущего пользователя
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    # Поле following - на кого подписываются
    # queryset - можно подписаться только на существующего пользователя
    # slug_field='username' - передаём username, а не ID
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = ('id', 'user', 'following')
        read_only_fields = ('id',)

    def validate_following(self, value):
        """
        Проверка: нельзя подписаться на самого себя.
        value - это пользователь, на которого пытаются подписаться.
        """
        # Получаем текущего пользователя из контекста запроса
        request = self.context.get('request')

        # Если текущий пользователь пытается подписаться на себя
        if request and request.user == value:
            # Выбрасываем ошибку с понятным сообщением
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )

        return value

    def validate(self, data):
        """
        Глобальная проверка: нельзя подписаться повторно.
        data - словарь с данными, которые прошли предыдущие проверки.
        """
        request = self.context.get('request')

        if request:
            # Проверяем, существует ли уже такая подписка в базе данных
            if Follow.objects.filter(
                user=request.user,           # текущий пользователь
                # пользователь, на кого подписываются
                following=data['following']
            ).exists():
                # Если существует - ошибка
                raise serializers.ValidationError(
                    'Вы уже подписаны на этого пользователя!'
                )

        return data
