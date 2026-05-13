# api_final

api final

## Описание

Проект представляет собой API для социальной сети Yatube.
API позволяет:

- Создавать, читать, обновлять и удалять посты
- Добавлять комментарии к постам
- Подписываться на других пользователей
- Просматривать сообщества (группы)

## Технологии

- Python 3.10
- Django 3.2.16
- Django REST Framework 3.14.0
- JWT-аутентификация
- SQLite (для разработки)

## Установка и запуск

1. Клонируйте репозиторий:
   git clone <ссылка на репозиторий>

2. Перейдите в папку проекта:
   cd api-final-yatube-ad-main/yatube_api

3.Создайте виртуальное окружение:
python -m venv venv

4.Активируйте виртуальное окружение:
source venv/Scripts/activate # Windows Git Bash

5.Установите зависимости:
pip install -r requirements.txt

6.Создайте миграции:
python manage.py makemigrations

7.Выполните миграции:
python manage.py migrate

8.Запустите сервер:
python manage.py runserver

## Примеры запросов к API

Получение JWT-токена
POST /api/v1/jwt/create/
Content-Type: application/json
{
"username": "user",
"password": "password"
}

Получение списка постов
GET /api/v1/posts/

Создание поста (требует авторизацию)
POST /api/v1/posts/
Authorization: Bearer <access_token>
Content-Type: application/json
{
"text": "Мой первый пост"
}

Подписка на пользователя
POST /api/v1/follow/
Authorization: Bearer <access_token>
Content-Type: application/json
{
"following": "username"
}

## Документация

После запуска сервера документация доступна по адресу:
http://127.0.0.1:8000/redoc/
