"""
Production Settings - Django Base Project

This module contains production-specific settings with security hardening.
CRITICAL: These settings are optimized for performance and security in production environments.

Key features:
- DEBUG mode DISABLED (critical for security)
- HTTPS/SSL enforcement with HSTS (HTTP Strict Transport Security)
- Secure cookies (session and CSRF) over HTTPS only
- Redis-based caching for improved performance
- Cache-based session storage for scalability
- SMTP email backend for real email delivery
- Comprehensive logging with file rotation and admin email alerts
- Static file serving with WhiteNoise (compression + caching)
- Database connection pooling and query timeouts
- Template caching for faster rendering
- Restricted CORS to specific allowed origins
- Production-ready Django Q configuration

---

Configurações de Produção - Projeto Django Base

Este módulo contém configurações específicas de produção com segurança reforçada.
CRÍTICO: Essas configurações são otimizadas para performance e segurança em ambientes de produção.

Recursos principais:
- Modo DEBUG DESABILITADO (crítico para segurança)
- Forçar HTTPS/SSL com HSTS (HTTP Strict Transport Security)
- Cookies seguros (sessão e CSRF) apenas via HTTPS
- Cache baseado em Redis para melhor performance
- Armazenamento de sessão baseado em cache para escalabilidade
- Backend de email SMTP para entrega real de emails
- Logging abrangente com rotação de arquivos e alertas de email para admin
- Servir arquivos estáticos com WhiteNoise (compressão + cache)
- Pool de conexões de banco de dados e timeouts de query
- Cache de templates para renderização mais rápida
- CORS restrito a origens permitidas específicas
- Configuração Django Q pronta para produção

Usage / Uso:
export DJANGO_SETTINGS_MODULE=django_base.settings.prod
"""

from .base import *  # noqa: F403

# Debug Mode / Modo Debug

# Force DEBUG to False in production (CRITICAL!)
# Força DEBUG como False em produção (CRÍTICO!)
DEBUG = False

# Security Settings (CRITICAL for Production)
# Configurações de Segurança (CRÍTICAS para Produção)

# HTTPS/SSL Settings
# Configurações HTTPS/SSL

# Redirect all HTTP traffic to HTTPS (prevents man-in-the-middle attacks)
# Redireciona todo tráfego HTTP para HTTPS (previne ataques man-in-the-middle)
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)  # noqa: F405

# Only transmit cookies over HTTPS (prevents cookie theft over HTTP)
# Transmite cookies apenas via HTTPS (previne roubo de cookies via HTTP)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HTTP Strict Transport Security (HSTS)
# Forces browser to use HTTPS for 1 year (even if user types http://)
# Força o navegador a usar HTTPS por 1 ano (mesmo que usuário digite http://)
SECURE_HSTS_SECONDS = 31536000  # 1 year / 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = (
    True  # Apply to all subdomains / Aplica a todos subdomínios
)
SECURE_HSTS_PRELOAD = (
    True  # Allow browser HSTS preload / Permite HSTS preload do navegador
)

# Additional Security Headers
# Cabeçalhos de Segurança Adicionais
SECURE_BROWSER_XSS_FILTER = True  # Enable XSS filtering / Habilita filtro XSS
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME type sniffing / Previne MIME sniffing
X_FRAME_OPTIONS = "DENY"  # Prevent clickjacking / Previne clickjacking
SECURE_REFERRER_POLICY = (
    "same-origin"  # Control referrer header / Controla header referrer
)

# CSRF Trusted Origins for CORS
# Origens Confiáveis CSRF para CORS
CSRF_TRUSTED_ORIGINS = config(  # noqa: F405
    "CSRF_TRUSTED_ORIGINS",
    cast=Csv(),  # noqa: F405
    default="https://yourdomain.com,https://www.yourdomain.com",
)

# Cache Configuration (Redis)
# Configuração de Cache (Redis)
# High-performance caching using Redis for faster response times
# Cache de alta performance usando Redis para tempos de resposta mais rápidos

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": config("REDIS_URL", default="redis://redis:6379/0"),  # noqa: F405
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                # Maximum connections to Redis
                # Máximo de conexões para Redis
                "max_connections": 50,
                # Retry on timeout for reliability
                # Retry em timeout para confiabilidade
                "retry_on_timeout": True,
            },
            # Connection and socket timeouts in seconds
            # Timeouts de conexão e socket em segundos
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
        },
        # Prefix all cache keys to avoid collisions
        # Prefixo para todas as chaves de cache para evitar colisões
        "KEY_PREFIX": "django_base",
        # Default cache timeout: 5 minutes
        # Timeout padrão de cache: 5 minutos
        "TIMEOUT": 300,
    }
}

# Session Configuration
# Configuração de Sessão

# Use cache-based session storage for better performance and scalability
# Stores sessions in Redis instead of database for faster access
# Usa armazenamento de sessão baseado em cache para melhor performance e escalabilidade
# Armazena sessões no Redis ao invés do banco de dados para acesso mais rápido
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Session security settings
# Configurações de segurança de sessão
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access / Previne acesso JavaScript
SESSION_COOKIE_SAMESITE = "Lax"  # CSRF protection / Proteção CSRF
SESSION_COOKIE_AGE = 1209600  # 2 weeks / 2 semanas

# Email Configuration for Production
# Configuração de Email para Produção

# SMTP Configuration - Real email delivery using SMTP server
# Configuração SMTP - Entrega real de email usando servidor SMTP
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")  # noqa: F405
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)  # noqa: F405
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)  # noqa: F405
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")  # noqa: F405
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")  # noqa: F405
# Default "From" email address for outgoing messages
# Endereço "De" padrão para mensagens enviadas
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@yourdomain.com")  # noqa: F405
# Email address for server error notifications
# Endereço de email para notificações de erro do servidor
SERVER_EMAIL = config("SERVER_EMAIL", default="server@yourdomain.com")  # noqa: F405

# Logging Configuration for Production
# Configuração de Logging para Produção
# Comprehensive logging with file rotation, console output, and email alerts for errors
# Logging abrangente com rotação de arquivo, saída console, e alertas de email para erros

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
        # Console output for container logs
        # Saída console para logs de container
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        # Rotating file handler to prevent disk space issues
        # Handler de arquivo rotativo para prevenir problemas de espaço em disco
        "file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "django.log",  # noqa: F405
            "maxBytes": 1024 * 1024 * 15,  # 15MB per file / 15MB por arquivo
            "backupCount": 10,  # Keep 10 backup files / Manter 10 arquivos de backup
            "formatter": "verbose",
        },
        # Email admins on errors (only when DEBUG=False)
        # Envia email para admins em erros (apenas quando DEBUG=False)
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

# Use WhiteNoise for serving static files efficiently without needing a separate server
# WhiteNoise adds compression and long-term caching headers
# Usa WhiteNoise para servir arquivos estáticos eficientemente sem precisar de servidor separado
# WhiteNoise adiciona compressão e headers de cache de longo prazo
MIDDLEWARE.insert(  # noqa: F405
    MIDDLEWARE.index("django.middleware.security.SecurityMiddleware") + 1,  # noqa: F405
    "whitenoise.middleware.WhiteNoiseMiddleware",
)

# Enable GZip compression and caching for static files (reduces bandwidth and improves speed)
# Habilita compressão GZip e cache para arquivos estáticos (reduz largura de banda e melhora velocidade)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Database Optimization for Production
# Otimização de Banco de Dados para Produção

# Persistent database connections (connection pooling) - reuse connections for 10 minutes
# Reduces connection overhead and improves performance
# Conexões persistentes de banco de dados (pool de conexões) - reutiliza conexões por 10 minutos
# Reduz overhead de conexão e melhora performance
DATABASES["default"]["CONN_MAX_AGE"] = 600  # noqa: F405

# Additional database options
# Opções adicionais de banco de dados
DATABASES["default"]["OPTIONS"] = {  # noqa: F405
    "connect_timeout": 10,  # Connection timeout in seconds / Timeout de conexão em segundos
    "options": "-c statement_timeout=30000",  # 30 second query timeout / Timeout de query 30 segundos
}

# Performance Optimizations
# Otimizações de Performance

# Template caching for faster rendering - templates are compiled once and cached
# Significantly improves response times for template-heavy views
# Cache de templates para renderização mais rápida - templates são compilados uma vez e cacheados
# Melhora significativamente tempos de resposta para views pesadas em templates
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

# Ensure sync mode is disabled in production (tasks run asynchronously in background)
# Garante que modo sync está desabilitado em produção (tarefas rodam assincronamente em background)
Q_CLUSTER["sync"] = False  # noqa: F405

# Increase workers for production load (more workers = more concurrent tasks)
# Aumenta workers para carga de produção (mais workers = mais tarefas concorrentes)
Q_CLUSTER["workers"] = config("DJANGO_Q_WORKERS", default=8, cast=int)  # noqa: F405

# CORS Configuration for Production
# Configuração CORS para Produção

# Disable allow all origins (use specific origins only for security)
# Only allow requests from trusted frontend domains
# Desabilita permitir todas as origens (usa apenas origens específicas para segurança)
# Permite apenas requisições de domínios frontend confiáveis
CORS_ALLOW_ALL_ORIGINS = False

# Restrict CORS to specific origins (whitelist your frontend domains)
# Restringe CORS para origens específicas (whitelist dos domínios frontend)
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
