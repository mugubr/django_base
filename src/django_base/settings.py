from pathlib import Path

from decouple import Csv, config

# Path to the project's root directory.
# Caminho para o diretório raiz do projeto.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Secret key for cryptographic signing. Keep this secret!
# Chave secreta para assinaturas criptográficas. Mantenha em segredo!
SECRET_KEY = config("SECRET_KEY")

# Debug mode. Should be False in production.
# Modo de depuração. Deve ser False em produção.
DEBUG = config("DEBUG", default=False, cast=bool)

# Hosts/domains that this Django site can serve.
# Hosts/domínios que este site Django pode servir.
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

INSTALLED_APPS = [
    "django_prometheus",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "corsheaders",
    "rest_framework",
    "django_q",
    "core",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "django_base.urls"

# Django REST Framework Configuration / Configuração do Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# CORS (Cross-Origin Resource Sharing) Configuration
# Configuração CORS (Cross-Origin Resource Sharing)
# List of origins that are authorized to make cross-site HTTP requests
# Lista de origens autorizadas a fazer requisições HTTP cross-site
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS", cast=Csv(), default="http://localhost:3000"
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "django_base.wsgi.application"
ASGI_APPLICATION = "django_base.asgi.application"

# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST", default="db"),
        "PORT": config("POSTGRES_PORT", default=5432, cast=int),
        "CONN_MAX_AGE": 600,  # Keep connections for 10 minutes
        "CONN_HEALTH_CHECKS": True,  # Django 4.1+ health checks
        "OPTIONS": {
            "connect_timeout": 10,
            "options": "-c statement_timeout=60000",  # 60s query timeout
        },
    }
}

# SQLAlchemy 2.0 Configuration
# Configuration for custom business logic with async support
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}"
    f"@{config('POSTGRES_HOST', default='db')}"
    f":{config('POSTGRES_PORT', default=5432, cast=int)}"
    f"/{config('POSTGRES_DB')}"
)

SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": 10,  # Base connection pool size
    "max_overflow": 10,  # Additional connections under load
    "pool_timeout": 30,  # Wait up to 30s for connection
    "pool_recycle": 3600,  # Recycle connections after 1 hour
    "pool_pre_ping": True,  # Verify connection health before checkout
    "pool_use_lifo": True,  # Reuse recent connections (better caching)
    "echo": config("SQL_ECHO", default=False, cast=bool),  # SQL logging
    "echo_pool": False,  # Disable pool logging in production
}

# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# Internationalization / Internacionalização
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images) / Arquivos estáticos (CSS, JavaScript, Imagens)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = "staticfiles/"
if not DEBUG:
    STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "mediafiles/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django Q (Background Tasks) Configuration
# Configuração do Django Q (Tarefas em Background)
# https://django-q2.readthedocs.io/en/latest/
Q_CLUSTER = {
    "name": "meu_projeto_django",
    "workers": 4,
    "recycle": 500,
    "timeout": 60,
    "compress": True,
    "save_limit": 250,
    "queue_limit": 500,
    "cpu_affinity": 1,
    "label": "Django Q",
    "orm": "default",
}
