# Base Settings - Django Base Project
# Configurações Base - Projeto Django Base

# This module contains settings shared across all environments.
# Environment-specific settings are in dev.py and prod.py
#
# Este módulo contém configurações compartilhadas entre todos os ambientes.
# Configurações específicas de ambiente estão em dev.py e prod.py

from pathlib import Path

from decouple import Csv, config

# Core Settings / Configurações Core

# Path to the project's root directory
# Caminho para o diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Secret key for cryptographic signing. Keep this secret!
# Chave secreta para assinaturas criptográficas. Mantenha em segredo!
SECRET_KEY = config("SECRET_KEY")

# Debug mode. Should be False in production.
# Modo de depuração. Deve ser False em produção.
DEBUG = config("DEBUG", default=False, cast=bool)

# Hosts/domains that this Django site can serve
# Hosts/domínios que este site Django pode servir
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(), default="localhost,127.0.0.1")

# Application Definition / Definição de Aplicação

INSTALLED_APPS = [
    # Django Prometheus must be first for accurate metrics
    # Django Prometheus deve ser primeiro para métricas precisas
    "django_prometheus",
    # Django built-in apps
    # Apps integradas do Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    # Apps de terceiros
    "django_extensions",
    "corsheaders",
    "rest_framework",
    "django_filters",  # Note: package is django-filter but module is django_filters
    "django_q",
    "drf_spectacular",
    # Local apps
    # Apps locais
    "core",
]

MIDDLEWARE = [
    # CORS middleware must be as high as possible
    # Middleware CORS deve estar o mais alto possível
    "corsheaders.middleware.CorsMiddleware",
    # Prometheus middleware wraps all requests
    # Middleware Prometheus envolve todas as requisições
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    # Django security middleware
    # Middleware de segurança do Django
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Prometheus after middleware
    # Prometheus após middleware
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "django_base.urls"

# Templates Configuration / Configuração de Templates

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI/ASGI Configuration

WSGI_APPLICATION = "django_base.wsgi.application"
ASGI_APPLICATION = "django_base.asgi.application"

# Database Configuration / Configuração de Banco de Dados

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST", default="db"),
        "PORT": config("POSTGRES_PORT", default=5432, cast=int),
        # Connection pooling and performance settings
        # Configurações de pool de conexões e performance
        "CONN_MAX_AGE": config("DB_CONN_MAX_AGE", default=600, cast=int),
        "OPTIONS": {
            "connect_timeout": 10,
        },
    }
}

# Password Validation / Validação de Senha

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        )
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization / Internacionalização

LANGUAGE_CODE = config("LANGUAGE_CODE", default="en-us")
TIME_ZONE = config("TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True

# Static Files (CSS, JavaScript, Images)
# Arquivos Estáticos (CSS, JavaScript, Imagens)

STATIC_URL = "staticfiles/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = []

MEDIA_URL = "mediafiles/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

# Default Primary Key Field Type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework Configuration
# Configuração do Django REST Framework

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    # Throttling to prevent API abuse
    # Limitação de taxa para prevenir abuso da API
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": config("THROTTLE_ANON", default="100/hour"),
        "user": config("THROTTLE_USER", default="1000/hour"),
    },
}

# DRF Spectacular (API Documentation) Configuration
# Configuração DRF Spectacular (Documentação da API)

SPECTACULAR_SETTINGS = {
    "TITLE": "Django Base API",
    "DESCRIPTION": "API documentation for Django Base Project",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
}

# CORS Configuration / Configuração CORS

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    cast=Csv(),
    default="http://localhost:3000,http://127.0.0.1:3000",
)

CORS_ALLOW_CREDENTIALS = True

# CSRF Trusted Origins / Origens Confiáveis CSRF
# Required for cross-origin POST requests
# Necessário para requisições POST cross-origin
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    cast=Csv(),
    default="http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000",
)

# Django Q (Background Tasks) Configuration
# Configuração do Django Q (Tarefas em Background)

Q_CLUSTER = {
    "name": "django_base",
    "workers": config("DJANGO_Q_WORKERS", default=4, cast=int),
    "recycle": 500,
    "timeout": 60,
    "compress": True,
    "save_limit": 250,
    "queue_limit": 500,
    "cpu_affinity": 1,
    "label": "Django Q",
    "orm": "default",
    # Redis configuration for Django Q
    # Configuração Redis para Django Q
    "redis": {
        "host": config("REDIS_HOST", default="redis"),
        "port": config("REDIS_PORT", default=6379, cast=int),
        "db": config("REDIS_DB", default=0, cast=int),
    },
}

# Authentication Configuration
# Configuração de Autenticação

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/admin/login/"
LOGOUT_REDIRECT_URL = "/"
