from pathlib import Path
from datetime import timedelta

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ (в продакшене нужно менять!)
SECRET_KEY = 'hhz7l-ltdismtf@bzyz+rple7*s*w$jak%whj@(@u0eok^f9k4'

# Режим отладки (только для разработки)
DEBUG = True

# Разрешённые хосты
ALLOWED_HOSTS = []

# Установленные приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Сторонние приложения
    'rest_framework',           # Django REST Framework
    'rest_framework.authtoken',  # Для токенов (не обязательно, но пусть будет)

    # Наши приложения
    'api.apps.ApiConfig',       # API приложение
    'posts.apps.PostsConfig',   # Posts приложение
]

# Добавляем Djoser для JWT (нужно установить через pip)
# Сначала выполни: pip install djoser
# INSTALLED_APPS.append('djoser')

# Промежуточное ПО (middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Корневой URLconf
ROOT_URLCONF = 'yatube_api.urls'

# Директория с шаблонами
TEMPLATES_DIR = BASE_DIR / 'templates'

# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI приложение
WSGI_APPLICATION = 'yatube_api.wsgi.application'

# Настройки базы данных (SQLite для разработки)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Валидаторы паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Язык и часовой пояс
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Статические файлы (CSS, JS, изображения)
STATIC_URL = '/static/'
STATICFILES_DIRS = ((BASE_DIR / 'static/'),)

# Настройки REST Framework
REST_FRAMEWORK = {
    # Классы разрешений по умолчанию
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    # Классы аутентификации
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT аутентификация
    ],
    # Пагинация - КОММЕНТИРУЕМ, чтобы группы и подписки возвращали список
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 10,
    # Фильтрация
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ],
}

# Настройки Simple JWT (время жизни токенов)
SIMPLE_JWT = {
    # Access токен живёт 1 день
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    # Refresh токен живёт 7 дней
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Настройки Djoser (если используем)
DJOSER = {
    'PERMISSIONS': {
        # Информация о пользователе только для авторизованных
        'user': ['rest_framework.permissions.IsAuthenticated'],
        'user_list': ['rest_framework.permissions.IsAuthenticated'],
    }
}

# Автоматическое поле первичного ключа
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
