# Production Settings - Django Base Project
# Configurações de Produção - Projeto Django Base

# This module contains production-specific settings with security hardening.
# These settings are optimized for performance and security.
#
# Este módulo contém configurações específicas de produção com segurança reforçada.
# Essas configurações são otimizadas para performance e segurança.
#
# Usage / Uso:
# export DJANGO_SETTINGS_MODULE=django_base.settings.prod

from .base import *  # noqa: F403

# Debug Mode / Modo Debug

# Force DEBUG to False in production (CRITICAL!)
# Força DEBUG como False em produção (CRÍTICO!)
DEBUG = False

# Security Settings (CRITICAL for Production)
# Configurações de Segurança (CRÍTICAS para Produção)

# HTTPS/SSL Settings
# Configurações HTTPS/SSL
# Redirect all HTTP traffic to HTTPS
# Redireciona todo tráfego HTTP para HTTPS
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)  # noqa: F405

# Only transmit cookies over HTTPS
# Transmite cookies apenas via HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HTTP Strict Transport Security (HSTS)
# Força o navegador a usar HTTPS por 1 ano
# Forces browser to use HTTPS for 1 year
SECURE_HSTS_SECONDS = 31536000  # 1 year / 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Additional Security Headers
# Cabeçalhos de Segurança Adicionais
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"

# CSRF Trusted Origins for CORS
# Origens Confiáveis CSRF para CORS
CSRF_TRUSTED_ORIGINS = config(  # noqa: F405
    "CSRF_TRUSTED_ORIGINS",
    cast=Csv(),  # noqa: F405
    default="https://yourdomain.com,https://www.yourdomain.com",
)

# Cache Configuration (Redis)
# Configuração de Cache (Redis)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": config("REDIS_URL", default="redis://redis:6379/0"),  # noqa: F405
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 50,
                "retry_on_timeout": True,
            },
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
        },
        "KEY_PREFIX": "django_base",
        "TIMEOUT": 300,  # 5 minutes default / 5 minutos padrão
    }
}

# Session Configuration
# Configuração de Sessão

# Use cache-based session storage for better performance
# Usa armazenamento de sessão baseado em cache para melhor performance
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Session security settings
# Configurações de segurança de sessão
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 1209600  # 2 weeks / 2 semanas

# Email Configuration for Production
# Configuração de Email para Produção

# SMTP Configuration
# Configuração SMTP
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")  # noqa: F405
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)  # noqa: F405
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)  # noqa: F405
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")  # noqa: F405
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")  # noqa: F405
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@yourdomain.com")  # noqa: F405
SERVER_EMAIL = config("SERVER_EMAIL", default="server@yourdomain.com")  # noqa: F405

# Logging Configuration for Production
# Configuração de Logging para Produção

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "django.log",  # noqa: F405
            "maxBytes": 1024 * 1024 * 15,  # 15MB
            "backupCount": 10,
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file", "mail_admins"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["mail_admins", "file"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["file", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "core": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Admin Configuration
# Configuração do Admin

# Email addresses that get error notifications
# Endereços de email que recebem notificações de erro
ADMINS = [
    ("Admin", config("ADMIN_EMAIL", default="admin@yourdomain.com")),  # noqa: F405
]

MANAGERS = ADMINS

# Static Files Configuration for Production
# Configuração de Arquivos Estáticos para Produção

# Use whitenoise for serving static files efficiently
# Usa whitenoise para servir arquivos estáticos eficientemente
MIDDLEWARE.insert(  # noqa: F405
    MIDDLEWARE.index("django.middleware.security.SecurityMiddleware") + 1,  # noqa: F405
    "whitenoise.middleware.WhiteNoiseMiddleware",
)

# Enable GZip compression and caching for static files
# Habilita compressão GZip e cache para arquivos estáticos
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Database Optimization for Production
# Otimização de Banco de Dados para Produção

# Persistent database connections (connection pooling)
# Conexões persistentes de banco de dados (pool de conexões)
DATABASES["default"]["CONN_MAX_AGE"] = 600  # noqa: F405

# Additional database options
# Opções adicionais de banco de dados
DATABASES["default"]["OPTIONS"] = {  # noqa: F405
    "connect_timeout": 10,
    "options": "-c statement_timeout=30000",  # 30 second query timeout
}

# Performance Optimizations
# Otimizações de Performance

# Template caching for faster rendering
# Cache de templates para renderização mais rápida
TEMPLATES[0]["OPTIONS"]["loaders"] = [  # noqa: F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    ),
]

# Error Monitoring (Sentry Integration)
# Monitoramento de Erros (Integração Sentry)

# Uncomment and configure if using Sentry
# Descomente e configure se usar Sentry
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
#
# sentry_sdk.init(
#     dsn=config("SENTRY_DSN", default=""),
#     integrations=[DjangoIntegration()],
#     traces_sample_rate=0.1,
#     send_default_pii=False,
#     environment=config("ENVIRONMENT", default="production"),
# )

# Django Q Configuration for Production
# Configuração Django Q para Produção

# Ensure sync mode is disabled in production
# Garante que modo sync está desabilitado em produção
Q_CLUSTER["sync"] = False  # noqa: F405

# Increase workers for production load
# Aumenta workers para carga de produção
Q_CLUSTER["workers"] = config("DJANGO_Q_WORKERS", default=8, cast=int)  # noqa: F405

# CORS Configuration for Production
# Configuração CORS para Produção

# Disable allow all origins (use specific origins only)
# Desabilita permitir todas as origens (usa apenas origens específicas)
CORS_ALLOW_ALL_ORIGINS = False

# Restrict CORS to specific origins
# Restringe CORS para origens específicas
CORS_ALLOWED_ORIGINS = config(  # noqa: F405
    "CORS_ALLOWED_ORIGINS",
    cast=Csv(),  # noqa: F405
    default="https://yourdomain.com,https://www.yourdomain.com",
)

# Content Security Policy (Optional but Recommended)
# Política de Segurança de Conteúdo (Opcional mas Recomendado)

# Uncomment if using django-csp
# Descomente se usar django-csp
# CSP_DEFAULT_SRC = ("'self'",)
# CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
# CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
# CSP_IMG_SRC = ("'self'", "data:", "https:")
# CSP_FONT_SRC = ("'self'",)
