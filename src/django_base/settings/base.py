"""
Base Settings - Django Base Project

This module contains settings shared across all environments (dev, prod, staging).
Environment-specific settings should be defined in their respective modules (dev.py, prod.py).

Key features:
- Core Django configuration (apps, middleware, templates)
- Database setup with PostgreSQL
- REST Framework with pagination and throttling
- CORS and CSRF security configuration
- Background task processing with Django Q
- API documentation with DRF Spectacular
- Prometheus metrics integration

---

Configurações Base - Projeto Django Base

Este módulo contém configurações compartilhadas entre todos os ambientes (dev, prod, staging).
Configurações específicas de ambiente devem ser definidas em seus respectivos módulos (dev.py, prod.py).

Recursos principais:
- Configuração core do Django (apps, middleware, templates)
- Setup de banco de dados com PostgreSQL
- REST Framework com paginação e limitação de taxa
- Configuração de segurança CORS e CSRF
- Processamento de tarefas em background com Django Q
- Documentação de API com DRF Spectacular
- Integração de métricas Prometheus
"""

from datetime import timedelta
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
# Django apps installed in this project, order matters for some apps
# Apps Django instaladas neste projeto, ordem importa para algumas apps

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

# Middleware Stack / Pilha de Middleware
# Order is critical: each middleware processes requests top-to-bottom and responses bottom-to-top
# Ordem é crítica: cada middleware processa requests de cima para baixo e responses de baixo para cima

MIDDLEWARE = [
    # CORS middleware must be as high as possible to handle preflight requests
    # Middleware CORS deve estar o mais alto possível para tratar requisições preflight
    "corsheaders.middleware.CorsMiddleware",
    # Prometheus middleware wraps all requests for metrics collection
    # Middleware Prometheus envolve todas as requisições para coletar métricas
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    # Django security middleware (HTTPS redirect, HSTS, etc.)
    # Middleware de segurança do Django (redirect HTTPS, HSTS, etc.)
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # Locale middleware for i18n (must be after SessionMiddleware)
    # Middleware de locale para i18n (deve estar após SessionMiddleware)
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Prometheus after middleware for response timing
    # Prometheus após middleware para timing de resposta
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
                # Custom context processor for portfolio settings
                # Processador de contexto customizado para configurações do portfolio
                "core.context_processors.portfolio_settings",
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
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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
# Language code for this installation. Options: 'en', 'pt-br', etc.
# Código de idioma para esta instalação. Opções: 'en', 'pt-br', etc.
LANGUAGE_CODE = config("LANGUAGE_CODE", default="pt-br")

# Time zone for this installation / Fuso horário para esta instalação
TIME_ZONE = config("TIME_ZONE", default="America/Sao_Paulo")

# Enable Django translation system / Habilitar sistema de tradução do Django
USE_I18N = True

# Enable timezone-aware datetimes / Habilitar datetimes com timezone
USE_TZ = True

# Languages supported by this application / Idiomas suportados por esta aplicação
LANGUAGES = [
    ("pt-br", "Português (Brasil)"),
    ("en", "English"),
]

# Path to locale files for translations / Caminho para arquivos de locale para traduções
LOCALE_PATHS = [
    BASE_DIR / "locale",
]

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
        "rest_framework_simplejwt.authentication.JWTAuthentication",
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
# Cross-Origin Resource Sharing allows frontend apps to make requests to this API
# Cross-Origin Resource Sharing permite apps frontend fazerem requisições para esta API

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    cast=Csv(),
    default="http://localhost:3000,http://127.0.0.1:3000",
)

# Allow cookies to be sent in cross-origin requests (needed for session auth)
# Permite cookies em requisições cross-origin (necessário para autenticação de sessão)
CORS_ALLOW_CREDENTIALS = True

# CSRF Trusted Origins / Origens Confiáveis CSRF
# Required for cross-origin POST requests with CSRF protection
# Django checks if the origin matches these trusted origins
# Necessário para requisições POST cross-origin com proteção CSRF
# Django verifica se a origem corresponde a estas origens confiáveis
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    cast=Csv(),
    default="http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000",
)

# Django Q (Background Tasks) Configuration
# Configuração do Django Q (Tarefas em Background)
# Used for async task processing (emails, reports, data processing, etc.)
# Usado para processamento assíncrono de tarefas (emails, relatórios, processamento de dados, etc.)

Q_CLUSTER = {
    "name": "django_base",
    # Number of worker processes for task execution
    # Número de processos worker para execução de tarefas
    "workers": config("DJANGO_Q_WORKERS", default=4, cast=int),
    # Recycle workers after N tasks to prevent memory leaks
    # Recicla workers após N tarefas para prevenir vazamento de memória
    "recycle": 500,
    # Task timeout in seconds
    # Timeout de tarefa em segundos
    "timeout": 60,
    # Compress task data in Redis
    # Comprime dados de tarefa no Redis
    "compress": True,
    # Maximum number of successful tasks to keep
    # Número máximo de tarefas bem-sucedidas para manter
    "save_limit": 250,
    # Maximum number of tasks in queue
    # Número máximo de tarefas na fila
    "queue_limit": 500,
    "cpu_affinity": 1,
    "label": "Django Q",
    # Use Django ORM for task storage
    # Usa Django ORM para armazenamento de tarefas
    "orm": "default",
    # Redis configuration for task broker
    # Configuração Redis para broker de tarefas
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

# Simple JWT Configuration / Configuração do Simple JWT
# JWT (JSON Web Token) authentication for REST API
# Autenticação JWT (JSON Web Token) para API REST

SIMPLE_JWT = {
    # Access token lifetime / Tempo de vida do token de acesso
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=config("JWT_ACCESS_TOKEN_MINUTES", default=60, cast=int)
    ),
    # Refresh token lifetime / Tempo de vida do token de refresh
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=config("JWT_REFRESH_TOKEN_DAYS", default=7, cast=int)
    ),
    # Automatically rotate refresh tokens on use / Rotaciona automaticamente tokens de refresh ao usar
    "ROTATE_REFRESH_TOKENS": True,
    # Blacklist refresh tokens after rotation / Adiciona tokens de refresh à blacklist após rotação
    "BLACKLIST_AFTER_ROTATION": True,
    # Algorithm for signing tokens / Algoritmo para assinar tokens
    "ALGORITHM": "HS256",
    # Signing key (uses SECRET_KEY by default) / Chave de assinatura (usa SECRET_KEY por padrão)
    "SIGNING_KEY": SECRET_KEY,
    # Token prefix in Authorization header / Prefixo do token no header Authorization
    "AUTH_HEADER_TYPES": ("Bearer",),
    # User ID field / Campo de ID do usuário
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    # Token type / Tipo de token
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}
