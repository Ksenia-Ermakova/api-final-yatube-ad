# Импортируем админ-панель Django
from django.contrib import admin

# Импортируем наши модели (ДОБАВЬ Group в импорт!)
from .models import Post, Comment, Follow, Group


# Класс для настройки отображения постов в админке
@admin.register(Post)  # Декоратор регистрирует модель в админке
class PostAdmin(admin.ModelAdmin):
    """
    Настройка отображения модели Post в админке.
    """
    # list_display - какие поля показывать в списке записей
    list_display = ('id', 'text', 'author', 'pub_date')
    # list_filter - фильтры справа
    list_filter = ('author', 'pub_date')
    # search_fields - поиск по этим полям
    # author__username - по имени автора
    search_fields = ('text', 'author__username')
    # ordering - сортировка в админке
    ordering = ('-pub_date',)


# Регистрируем модель Comment в админке
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Какие поля показывать
    list_display = ('id', 'post', 'author', 'text', 'created')
    # Фильтры
    list_filter = ('author', 'created')
    # Поиск
    search_fields = ('text', 'author__username', 'post__text')


# Регистрируем модель Follow в админке
@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    # Какие поля показывать
    list_display = ('id', 'user', 'following')
    # Фильтры
    list_filter = ('user', 'following')
    # Поиск
    search_fields = ('user__username', 'following__username')


# Регистрируем модель Group в админке
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    prepopulated_fields = {'slug': ('title',)}  # slug автоматически из title
    search_fields = ('title', 'description')
