from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'django_celery_results',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'apps.api',
    'apps.core',
    'apps.processes',
    'apps.robots',
    'apps.tasks',
    'apps.items',
    'apps.values',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'apps.core.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'apps.core.wsgi.application'



# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'sgautomacao'),
        'USER': os.getenv('POSTGRES_USER', 'wtime'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'wtimepassword'),
        'HOST': os.getenv('DB_HOST', 'db'),  # O hostname definido no docker-compose é 'db'
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

LOGIN_URL = '/login/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = (
    str(Path.joinpath(BASE_DIR, 'static')),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Arquivos de mídia (upload de imagens, documentos, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTOSCHEMA OPENAPI 

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ],
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': (
                'Token JWT para autenticação.\n\n'
                '**Instruções para uso:**\n'
                '1. Primeiro, obtenha um token através do endpoint de login.\n'
                '2. Insira o token JWT no campo "Value" no seguinte formato: `Bearer <seu_token>`.\n'
                '3. Certifique-se de incluir a palavra "Bearer" antes do token, separada por um espaço.\n\n'
                '**Exemplo de Cabeçalho HTTP:**\n'
                '`Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI...`'
            ),
        }
    },
    'DEFAULT_AUTO_SCHEMA_CLASS': 'apps.utils.custom_auto_schema.CustomSwaggerAutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # Define o tempo de expiração do token de acesso
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Define o tempo de expiração do token de atualização
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',
}

# CELERY SETTINGS
# Configuración general de Celery

# URL del broker de mensajes de Celery
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'amqp://guest:guest@rabbitmq:5672//')


# Tipos de contenido aceptados por Celery al recibir mensajes de tareas
CELERY_ACCEPT_CONTENT = ['json', 'pickle']

# Serializador utilizado para los resultados de las tareas
CELERY_RESULT_SERIALIZER = 'pickle'

# Serializador utilizado para las tareas
CELERY_TASK_SERIALIZER = 'pickle'

# Zona horaria utilizada por Celery
CELERY_TIME_ZONE = 'America/Sao_Paulo'

# CELERY RESULTS
# Configuración del backend para almacenar los resultados de las tareas
# (usando Django)

# Backend de resultados utilizando la base de datos de Django
CELERY_RESULT_BACKEND = 'django-db'

# Backend de caché utilizando el framework de caché de Django
CELERY_CACHE_BACKEND = 'django-cache'

# CELERY BEAT
# Configuración para Celery Beat, el planificador de tareas:

# Indica a Celery Beat que utilice el planificador de bases de datos
# para programar y ejecutar las tareas
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
