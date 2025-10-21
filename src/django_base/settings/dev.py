"""
Development Settings - Django Base Project

This module contains development-specific settings optimized for local development.
CRITICAL: Never use these settings in production - they disable security features!

Key features:
- DEBUG mode enabled for detailed error pages
- All hosts allowed for development convenience
- Console email backend (prints to terminal)
- Dummy cache backend (no caching for easier debugging)
- Verbose logging with SQL query debugging
- Browsable API renderer for REST Framework
- Security settings disabled (HTTPS, HSTS, secure cookies)
- CORS allows all origins

---

Configurações de Desenvolvimento - Projeto Django Base

Este módulo contém configurações específicas de desenvolvimento otimizadas para desenvolvimento local.
CRÍTICO: Nunca use essas configurações em produção - elas desabilitam recursos de segurança!

Recursos principais:
- Modo DEBUG habilitado para páginas de erro detalhadas
- Todos os hosts permitidos para conveniência de desenvolvimento
- Backend de email console (imprime no terminal)
- Backend de cache dummy (sem cache para debug mais fácil)
- Logging verbose com debug de queries SQL
- Renderer de API navegável para REST Framework
- Configurações de segurança desabilitadas (HTTPS, HSTS, cookies seguros)
- CORS permite todas as origens

Usage / Uso:
export DJANGO_SETTINGS_MODULE=django_base.settings.dev
"""

from .base import *  # noqa: F403

# Debug Mode / Modo Debug

# Force DEBUG to True in development
# Força DEBUG como True em desenvolvimento
DEBUG = True

# Allow all hosts in development for convenience
# Permite todos os hosts em desenvolvimento por conveniência
ALLOWED_HOSTS = ["*"]

# Development-Specific Apps / Apps Específicas de Desenvolvimento

# Django Debug Toolbar is enabled by default in development
# Django Debug Toolbar está habilitado por padrão em desenvolvimento
INSTALLED_APPS += [  # noqa: F405
    "debug_toolbar",
]

# Development Middleware / Middleware de Desenvolvimento
MIDDLEWARE = [  # noqa: RUF005
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE  # noqa: F405

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

# Print emails to console instead of sending (useful for testing email features)
# Imprime emails no console ao invés de enviar (útil para testar funcionalidades de email)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Cache Configuration for Development
# Configuração de Cache para Desenvolvimento

# Use dummy cache in development (no caching, always fresh data)
# This prevents cached data from hiding bugs during development
# Usa cache dummy em desenvolvimento (sem cache, sempre dados frescos)
# Isso previne que dados em cache escondam bugs durante desenvolvimento
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Or use Redis if you want to test caching locally
# Uncomment below to enable real caching in development
# Ou use Redis se quiser testar cache localmente
# Descomente abaixo para habilitar cache real em desenvolvimento
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/0",
#     }
# }

# Logging Configuration for Development
# Configuração de Logging para Desenvolvimento
# Verbose logging to help debug issues during development
# Logging verbose para ajudar a debugar problemas durante desenvolvimento

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            # Includes timestamp, module name, and message
            # Inclui timestamp, nome do módulo, e mensagem
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
        # Database backend logger shows SQL queries when set to DEBUG
        # Logger de backend de banco mostra queries SQL quando definido como DEBUG
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",  # Set to DEBUG to see SQL queries / DEBUG para ver queries SQL
            "propagate": False,
        },
        # Local app logger
        # Logger de app local
        "core": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# CORS Configuration for Development
# Configuração CORS para Desenvolvimento

# Allow all origins in development for maximum flexibility
# Useful when testing with different frontend URLs/ports
# Permite todas as origens em desenvolvimento para máxima flexibilidade
# Útil ao testar com diferentes URLs/portas de frontend
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

# WARNING: These security features are DISABLED for development convenience
# They MUST be enabled in production for security!
# AVISO: Estas funcionalidades de segurança estão DESABILITADAS para conveniência de desenvolvimento
# Elas DEVEM ser habilitadas em produção para segurança!

SECURE_SSL_REDIRECT = (
    False  # Don't redirect HTTP to HTTPS / Não redireciona HTTP para HTTPS
)
SESSION_COOKIE_SECURE = False  # Allow cookies over HTTP / Permite cookies via HTTP
CSRF_COOKIE_SECURE = (
    False  # Allow CSRF cookies over HTTP / Permite cookies CSRF via HTTP
)
SECURE_HSTS_SECONDS = 0  # Disable HSTS / Desabilita HSTS
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Django Q Configuration for Development
# Configuração Django Q para Desenvolvimento

# Use sync mode for easier debugging (tasks run synchronously in same process)
# Set DJANGO_Q_SYNC=True in .env to enable synchronous mode
# Usa modo sync para debugging mais fácil (tarefas rodam sincronamente no mesmo processo)
# Defina DJANGO_Q_SYNC=True no .env para habilitar modo síncrono
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

# Environment Variables Validation (Development) - OPTIONAL
# Validação de Variáveis de Ambiente (Desenvolvimento) - OPCIONAL
#
# To enable environment validation, set ENABLE_ENV_VALIDATION=true in your .env file
# Para habilitar validação de ambiente, defina ENABLE_ENV_VALIDATION=true no seu .env
#
# Uncomment the code below to enable validation:
# Descomente o código abaixo para habilitar a validação:
#
# import os
# import sys
#
# if "test" not in sys.argv and os.getenv("ENABLE_ENV_VALIDATION", "false").lower() == "true":
#     from django_base.settings.env_validator import validate_environment
#
#     validate_environment(
#         environment="development",
#         debug=DEBUG,
#         secret_key=SECRET_KEY,
#         allowed_hosts=ALLOWED_HOSTS,
#         database_config=DATABASES["default"],
#         secure_ssl_redirect=SECURE_SSL_REDIRECT,
#         session_cookie_secure=SESSION_COOKIE_SECURE,
#         csrf_cookie_secure=CSRF_COOKIE_SECURE,
#     )
