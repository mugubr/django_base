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
    }
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
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "mediafiles/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django Q (Background Tasks) Configuration
# Configuração do Django Q (Tarefas em Background)
# https://django-q2.readthedocs.io/en/latest/
Q_CLUSTER = {
    "name": "django_base",
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
