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
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

NGROK_DOMAIN = os.getenv("NGROK_DOMAIN")

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

if NGROK_DOMAIN:
    ALLOWED_HOSTS.append(NGROK_DOMAIN)

CORS_ALLOWED_ORIGINS = [
    'http://localhost',
    'http://127.0.0.1',
]

if NGROK_DOMAIN:
    CORS_ALLOWED_ORIGINS.append(f"https://{NGROK_DOMAIN}")


CORS_ALLOW_CREDENTIALS = True


CSRF_TRUSTED_ORIGINS = []
if NGROK_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(f"https://{NGROK_DOMAIN}")

# Application definition

INSTALLED_APPS = [
    'jazzmin',
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
    'apps.ai',
    'apps.alerts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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


# Configuração Jazzmin
JAZZMIN_SETTINGS = {
    "site_title": "Painel de Controle Wtime",  # Título do navegador
    "site_header": "Administração Wtime",  # Cabeçalho principal no Admin
    "site_brand": "Wtime",  # Branding da empresa no topo
    "site_logo": "assets/img_jazzmin/LogoHorizontal_Wtime_CorOficial-1.png",  # Caminho do logo
    "login_logo": "assets/img_jazzmin/wTIME-1.jpg",  # Logo na tela de login
    "login_logo_dark": "assets/img_jazzmin/LogoHorizontal_Wtime_CorOficial-1.png",  # Logo na tela de login no modo escuro

    "site_icon": "assets/img_jazzmin/LogoHorizontal_Wtime_CorOficial-1.png",  # Ícone do site
    "welcome_sign": "Bem-vindo ao painel de administração da Wtime",  # Texto na tela de login
    "copyright": "Wtime © 2024",  # Texto de copyright no rodapé

    # Links rápidos no topo (ações rápidas)
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Site", "url": "/", "new_window": True},
        {"model": "auth.User"},  # Link rápido para usuários
        {"app": "apps.ai"},  # Link rápido para seu app de IA
    ],

    # Configurações de modelos (organização na barra lateral)
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [
        "auth",
        "apps.tasks",
        "apps.ai",
        "apps.items",
    ],

    # Ícones dos apps (usando ícones do FontAwesome)
    "icons": {
        "auth": "fas fa-users-cog",             # Ícone para o app de autenticação
        "auth.user": "fas fa-user",             # Ícone para o modelo de usuário
        "auth.Group": "fas fa-users",           # Ícone para o modelo de grupo

        "ai.AIAssessment": "fas fa-brain",      # Ícone para o app de AI Assessments

        "django_celery_results.GroupResult": "fas fa-layer-group",   # Ícone para resultados de grupo do Celery
        "django_celery_results.TaskResult": "fas fa-tasks",    # Ícone para resultados de tarefas do Celery

        "items.Item": "fas fa-clipboard-list",  # Ícone para o app de itens

        "django_celery_beat.ClockedSchedule": "fas fa-clock",  # Ícone para tarefas agendadas por relógio
        "django_celery_beat.CrontabSchedule": "fas fa-calendar-alt",  # Ícone para crontabs
        "django_celery_beat.IntervalSchedule": "fas fa-hourglass-half",  # Ícone para intervalos de tarefas
        "django_celery_beat.SolarSchedule": "fas fa-sun",  # Ícone para eventos solares
        "django_celery_beat.PeriodicTask": "fas fa-calendar-check",  # Ícone para tarefas periódicas

        "processes.Process": "fas fa-cogs",     # Ícone para o app de processos

        "robots.Robot": "fas fa-robot",         # Ícone para o app de robôs

        "tasks.Task": "fas fa-tasks",           # Ícone para o app de tarefas

        "values.ShiftData": "fas fa-chart-line", # Ícone para o app de valores
    },

    # Configuração de estilo e temas
    "changeform_format": "horizontal_tabs",  # Exibição de formulários
    "changeform_format_overrides": {
        "auth.user": "collapsible",  # Formato de usuário em colapsos
    },
    "related_modal_active": True,  # Modal para foreign keys e related fields
    # 'show_ui_builder': True,
}


JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-primary navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": False
}