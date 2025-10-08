# Multi-Stage Dockerfile for Django Application
# Dockerfile Multi-Stage para Aplicação Django

# This Dockerfile uses multi-stage builds to create optimized images for both
# development and production environments, reducing image size and improving security.
# Este Dockerfile usa builds multi-stage para criar imagens otimizadas para ambientes
# de desenvolvimento e produção, reduzindo o tamanho da imagem e melhorando a segurança.

# Stage 1: Base Image

# Base stage with common configuration for all environments
# Stage base com configuração comum para todos os ambientes
FROM python:3.11-slim AS base

# Set working directory inside the container
# Define o diretório de trabalho dentro do container
WORKDIR /app

# Environment variables for Python optimization
# Variáveis de ambiente para otimização do Python
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies and clean up in single layer to reduce image size
# Instala dependências do sistema e limpa em uma única camada para reduzir o tamanho da imagem
RUN apt-get update && apt-get install -y --no-install-recommends \
    # PostgreSQL client library required by psycopg2
    # Biblioteca cliente do PostgreSQL necessária para psycopg2
    libpq5 \
    # GNU gettext for i18n compilemessages
    # GNU gettext para compilemessages i18n
    gettext \
    # Cleanup APT cache to reduce image size
    # Limpa cache do APT para reduzir tamanho da imagem
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager (faster than pip)
# Instala o gerenciador de pacotes uv (mais rápido que pip)
RUN pip install --no-cache-dir uv

# Stage 2: Development Dependencies

# Stage for development with all dev dependencies installed
# Stage para desenvolvimento com todas as dependências dev instaladas
FROM base AS dependencies-dev

# Copy dependency definition files
# These are copied first to leverage Docker's layer caching
# Copia arquivos de definição de dependências
# São copiados primeiro para aproveitar o cache de camadas do Docker
COPY ./pyproject.toml ./uv.lock* ./

# Create virtual environment and install ALL dependencies (production + dev)
# Install dependencies from pyproject.toml without the local package
# Cria ambiente virtual e instala TODAS as dependências (produção + dev)
# Instala dependências do pyproject.toml sem o pacote local
RUN uv venv && \
    uv pip install --python /app/.venv/bin/python \
    django>=5.2.7 \
    django-cors-headers>=4.9.0 \
    django-prometheus>=2.4.1 \
    django-q2>=1.8.0 \
    djangorestframework>=3.16.1 \
    gunicorn>=23.0.0 \
    psycopg2-binary>=2.9.10 \
    python-decouple>=3.8 \
    celery>=5.5.3 \
    django-environ>=0.12.0 \
    django-filter>=25.2 \
    redis>=6.4.0 \
    sentry-sdk>=2.39.0 \
    whitenoise>=6.11.0 \
    drf-spectacular>=0.28.0 \
    django-extensions>=4.1 \
    Pillow>=11.0.0 \
    coverage>=7.10.7 \
    pre-commit>=4.3.0 \
    ruff>=0.13.2 \
    watchdog>=6.0.0 \
    werkzeug>=3.1.3

# Stage 3: Production Dependencies

# Stage for production with only production dependencies
# Stage para produção com apenas dependências de produção
FROM base AS dependencies-prod

# Copy dependency definition files
# Copia arquivos de definição de dependências
COPY ./pyproject.toml ./uv.lock* ./

# Create virtual environment and install ONLY production dependencies
# This significantly reduces the final image size and attack surface
# Cria ambiente virtual e instala APENAS dependências de produção
# Isso reduz significativamente o tamanho final da imagem e a superfície de ataque
RUN uv venv && \
    uv pip install --python /app/.venv/bin/python \
    django>=5.2.7 \
    django-cors-headers>=4.9.0 \
    django-prometheus>=2.4.1 \
    django-q2>=1.8.0 \
    djangorestframework>=3.16.1 \
    gunicorn>=23.0.0 \
    psycopg2-binary>=2.9.10 \
    python-decouple>=3.8 \
    celery>=5.5.3 \
    django-environ>=0.12.0 \
    django-filter>=25.2 \
    redis>=6.4.0 \
    sentry-sdk>=2.39.0 \
    whitenoise>=6.11.0 \
    drf-spectacular>=0.28.0 \
    Pillow>=11.0.0 \
    django-extensions>=4.1

# Stage 4: Development Image

# Final stage for development environment
# Stage final para ambiente de desenvolvimento
FROM dependencies-dev AS development

# Copy entire project source code
# Copia todo o código-fonte do projeto
COPY . .

# Expose port 8000 for Django development server
# Expõe a porta 8000 para o servidor de desenvolvimento do Django
EXPOSE 8000

# Default command for development using runserver_plus from django-extensions
# Provides enhanced debugging features like Werkzeug debugger
# Comando padrão para desenvolvimento usando runserver_plus do django-extensions
# Fornece recursos aprimorados de debugging como debugger Werkzeug
CMD ["python", "manage.py", "runserver_plus", "0.0.0.0:8000"]

# Stage 5: Production Image

# Final stage for production environment with security hardening
# Stage final para ambiente de produção com segurança reforçada
FROM dependencies-prod AS production

# Create non-root user for security best practices
# Running as root in containers is a security risk
# Cria usuário não-root seguindo boas práticas de segurança
# Executar como root em containers é um risco de segurança
RUN groupadd -r django && useradd -r -g django django

# Create directory for logs with appropriate permissions
# Cria diretório para logs com permissões apropriadas
RUN mkdir -p /app/logs && chown django:django /app/logs

# Copy application code with proper ownership
# Copia código da aplicação com propriedade correta
COPY --chown=django:django . .

# Collect static files during build time (optimization)
# This eliminates the need to run collectstatic at runtime
# Coleta arquivos estáticos durante o build (otimização)
# Isso elimina a necessidade de executar collectstatic em runtime
RUN python manage.py collectstatic --noinput --clear || true

# Switch to non-root user
# All subsequent commands and the container process will run as this user
# Muda para usuário não-root
# Todos os comandos subsequentes e o processo do container rodarão como este usuário
USER django

# Expose port 8000 for Gunicorn WSGI server
# Expõe a porta 8000 para o servidor WSGI Gunicorn
EXPOSE 8000

# Health check to verify application is responding
# Docker/Kubernetes use this to determine container health
# Health check para verificar se a aplicação está respondendo
# Docker/Kubernetes usam isso para determinar a saúde do container
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/', timeout=2)" || exit 1

# Production command using Gunicorn with recommended settings
# - bind to 0.0.0.0:8000 to accept connections from outside container
# - workers: number of worker processes (recommended: 2-4 per core)
# - timeout: worker timeout in seconds (increase for slow endpoints)
# Comando de produção usando Gunicorn com configurações recomendadas
# - bind em 0.0.0.0:8000 para aceitar conexões de fora do container
# - workers: número de processos worker (recomendado: 2-4 por core)
# - timeout: timeout do worker em segundos (aumentar para endpoints lentos)
CMD ["gunicorn", "django_base.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info"]
