# Импортируем модель пользователя (встроенная в Django)
# get_user_model() получает активную модель пользователя (обычно это User)
from django.contrib.auth import get_user_model
from django.db import models  # Импортируем модуль для работы с БД

# Получаем модель пользователя (у нас она называется User)
User = get_user_model()


class Post(models.Model):
    """
    Модель поста (публикации).
    Каждый пост принадлежит автору и содержит текст, дату и картинку.
    """

    # Текст поста. TextField - для длинного текста.
    text = models.TextField()

    # Дата публикации. auto_now_add=True автоматич ставит текущ дату
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    # Автор поста. ForeignKey - связь "один ко многим" (один польз-много пост)
    # on_delete=models.CASCADE - если пользователя удалят, удалятся его посты
    # related_name='posts' -получить все посты пользова-ля: user.posts.all()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )

    # Картинка. ImageField - для загрузки изображений
    # upload_to='posts/' - картинки сохранятся в папке media/posts/
    # null=True, blank=True - поле необязательное
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True
    )

    # Поле group - связь с сообществом (может быть пустым)
    # on_delete=models.SET_NULL - если группу удалят, поле станет NULL
    # null=True, blank=True - поле необязательное
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )

    class Meta:
        """
        Meta - внутренний класс для настроек модели.
        Здесь мы указываем сортировку по умолчанию.
        """
        # ordering - сортировка. Минус= "по убыванию" (от новых к старым)
        # Без этого пагинация в API работать не будет!
        ordering = ('-pub_date',)

    def __str__(self):
        """
        Метод __str__ возвращает строковое представление объекта.
        Используется в админке и при отладке.
        """
        # Возвращаем первые 50 символов текста поста
        return self.text[:50]


class Comment(models.Model):
    """
    Модель комментария.
    Комментарий привязан к посту и к автору.
    """

    # Автор комментария. Связь с пользователем
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )

    # Пост, к которому оставлен комментарий
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )

    # Текст комментария
    text = models.TextField()

    # Дата создания. auto_now_add=True - автоматически при создании
    # db_index=True - создаёт индекс в БД для быстрого поиска
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        # Комментарии сортируем от старых к новым
        ordering = ('created',)

    def __str__(self):
        # Возвращаем первые 50 символов текста комментария
        return self.text[:50]


class Follow(models.Model):
    """
    Модель подписки.
    Пользователь (user) подписывается на другого пользователя (following).
    """

    # Кто подписывается. related_name='follower' - все подписки пользователя
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # При удалении пользо-ля удаляем его подписки
        related_name='follower'   # user.follower.all() - на кого подписан user
    )

    # На кого подписываются
    following = models.ForeignKey(
        User,
        # При удалении пользователя удаляем подписки на него
        on_delete=models.CASCADE,
        related_name='following'  # user.following.all() - кто подписан на user
    )

    class Meta:
        """
        Настройки модели.
        Здесь мы указываем, что пара (user, following) должна быть уникальной.
        Это запрещает повторные подписки.
        """
        # Важно! Используем UniqueConstraint, а не устаревший unique_together
        constraints = [
            models.UniqueConstraint(
                # Проверяем уникальность этой пары
                fields=['user', 'following'],
                name='unique_user_following'   # Имя ограничения
            )
        ]
        # Сортировка по умолчанию - по id подписки
        ordering = ('id',)

    def __str__(self):
        # Возвращаем читаемое описание подписки
        return f'{self.user} подписан на {self.following}'


class Group(models.Model):
    """
    Модель сообщества.
    Посты можно объединять в группы по интересам.
    """

    # Название группы (максимум 200 символов)
    title = models.CharField(max_length=200)

    # Уникальный идентификатор для URL (например, "python-developers")
    # unique=True - нельзя создать две группы с одинаковым slug
    slug = models.SlugField(max_length=50, unique=True)

    # Описание группы
    description = models.TextField()

    class Meta:
        # Сортировка по названию
        ordering = ('title',)

    def __str__(self):
        return self.title
