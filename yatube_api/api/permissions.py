"""
Классы разрешений для API Yatube.
Определяют, кто может делать какие запросы.
"""

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение:
    - Читать (GET) могут все (включая анонимов)
    - Создавать (POST) могут только авторизованные
    - Редактировать и удалять (PUT, PATCH, DELETE) может только автор
    """

    def has_permission(self, request, view):
        """
        Проверка ДО получения объекта (для списков и создания).
        """
        # Безопасные методы (GET, HEAD, OPTIONS) доступны всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Остальные методы (POST, PUT, DELETE) - только авторизованным
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Проверка ДЛЯ конкретного объекта.
        obj - это сам пост или комментарий.
        """
        # Чтение доступно всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Изменение и удаление - только автору
        return obj.author == request.user


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Простое разрешение:
    - Чтение (GET) - для всех
    - Всё остальное - только для авторизованных
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated


class IsAuthenticatedForFollow(permissions.BasePermission):
    """
    Разрешение для подписок:
    - ВСЕ запросы к /follow/ требуют авторизации
    - Анонимов не пускаем вообще
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated
