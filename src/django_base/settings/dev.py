# Development Settings - Django Base Project
# Configurações de Desenvolvimento - Projeto Django Base

# This module contains development-specific settings.
# Never use these settings in production!
#
# Este módulo contém configurações específicas para desenvolvimento.
# Nunca use essas configurações em produção!
#
# Usage / Uso:
# export DJANGO_SETTINGS_MODULE=django_base.settings.dev

from .base import *  # noqa: F403

# Debug Mode / Modo Debug

# Force DEBUG to True in development
# Força DEBUG como True em desenvolvimento
DEBUG = True

# Allow all hosts in development for convenience
# Permite todos os hosts em desenvolvimento por conveniência
ALLOWED_HOSTS = ["*"]

# Development-Specific Apps / Apps Específicas de Desenvolvimento

INSTALLED_APPS += [  # noqa: F405
    # Django Debug Toolbar for performance profiling
    # Django Debug Toolbar para profiling de performance
    # "debug_toolbar",  # Uncomment if you install it / Descomente se instalar
]

# Development Middleware / Middleware de Desenvolvimento

# MIDDLEWARE = [
#     "debug_toolbar.middleware.DebugToolbarMiddleware",
# ] + MIDDLEWARE
# Uncomment above if using debug toolbar
# Descomente acima se usar debug toolbar

# Debug Toolbar Configuration
# Configuração do Debug Toolbar

# Internal IPs for Debug Toolbar
# IPs internos para Debug Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

# Database Configuration for Development
# Configuração de Banco de Dados para Desenvolvimento

# Optionally use SQLite for faster local development
# Opcionalmente use SQLite para desenvolvimento local mais rápido
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# Email Configuration for Development
# Configuração de Email para Desenvolvimento

# Print emails to console instead of sending
# Imprime emails no console ao invés de enviar
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Cache Configuration for Development
# Configuração de Cache para Desenvolvimento

# Use dummy cache in development (no caching)
# Usa cache dummy em desenvolvimento (sem cache)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Or use Redis if you want to test caching locally
# Ou use Redis se quiser testar cache localmente
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/0",
#     }
# }

# Logging Configuration for Development
# Configuração de Logging para Desenvolvimento

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",  # Set to DEBUG to see SQL queries
            "propagate": False,
        },
        "core": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# CORS Configuration for Development
# Configuração CORS para Desenvolvimento

# Allow all origins in development
# Permite todas as origens em desenvolvimento
CORS_ALLOW_ALL_ORIGINS = True

# Django REST Framework for Development
# Django REST Framework para Desenvolvimento

# Add browsable API renderer for development
# Adiciona renderer de API navegável para desenvolvimento
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",  # Browsable API for development
]

# Security Settings (Disabled for Development)
# Configurações de Segurança (Desabilitadas para Desenvolvimento)

# These should be enabled in production!
# Estas devem ser habilitadas em produção!
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Django Q Configuration for Development
# Configuração Django Q para Desenvolvimento

# Use sync mode for easier debugging
# Usa modo sync para debugging mais fácil
Q_CLUSTER["sync"] = config("DJANGO_Q_SYNC", default=False, cast=bool)  # noqa: F405

# Performance Settings for Development
# Configurações de Performance para Desenvolvimento

# Template caching disabled for instant reload
# Cache de templates desabilitado para reload instantâneo
# TEMPLATES[0]["OPTIONS"]["loaders"] = [
#     "django.template.loaders.filesystem.Loader",
#     "django.template.loaders.app_directories.Loader",
# ]

# Development-Specific Variables
# Variáveis Específicas de Desenvolvimento

# Show detailed error pages
# Mostra páginas de erro detalhadas
DEBUG_PROPAGATE_EXCEPTIONS = True

# Print SQL queries (useful for debugging)
# Imprime queries SQL (útil para debugging)
# LOGGING["loggers"]["django.db.backends"]["level"] = "DEBUG"
