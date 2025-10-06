# Main URL Configuration - Django Base Project
# Configuração Principal de URLs - Projeto Django Base

# This module defines the main URL routing for the entire Django project with:
# - API endpoints (versioned)
# - Admin interface
# - Health check endpoints
# - Metrics endpoints for monitoring
# - Custom error handlers
# - Static/media file serving (development only)
#
# Este módulo define o roteamento principal de URLs para todo
# o projeto Django com:
# - Endpoints de API (versionados)
# - Interface administrativa
# - Endpoints de health check
# - Endpoints de métricas para monitoramento
# - Handlers de erro customizados
# - Servir arquivos estáticos/mídia (apenas desenvolvimento)

# Import custom error handlers from core app
# Importa handlers de erro customizados da app core
from core import views
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from django_base import settings

# URL Patterns
# Padrões de URL

urlpatterns = [
    # Admin Interface
    # Interface Administrativa
    # Django's built-in admin panel for content management
    # Painel administrativo integrado do Django para gerenciamento de conteúdo
    path("admin/", admin.site.urls),
    # Health Check Endpoint
    # Endpoint de Health Check
    # Used by Docker, Kubernetes, load balancers to monitor application health
    # Usado por Docker, Kubernetes, load balancers para monitorar saúde
    # da aplicação
    path("health/", views.health_check, name="health_check"),
    # Monitoring & Metrics
    # Monitoramento & Métricas
    # Prometheus metrics endpoint for application monitoring
    # Endpoint de métricas Prometheus para monitoramento da aplicação
    path("django-metrics/", include("django_prometheus.urls")),
    # API Endpoints
    # Endpoints da API
    # Versioned API endpoints (v1)
    # Endpoints da API versionados (v1)
    # Includes: /api/v1/products/, /api/v1/hello/, etc.
    # Inclui: /api/v1/products/, /api/v1/hello/, etc.
    path("api/v1/", include("core.urls")),
    # API information endpoint
    # Endpoint de informações da API
    path("api/info/", views.api_info, name="api_info"),
    # API Documentation (if using drf-spectacular)
    # Documentação da API (se usar drf-spectacular)
    # Uncomment if you have drf-spectacular installed
    # Descomente se tiver drf-spectacular instalado
    # from drf_spectacular.views import SpectacularAPIView,
    # SpectacularSwaggerView
    # path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"),
    # name="api-docs"),
]

# Development-Only URLs
# URLs Apenas para Desenvolvimento

# Serve media files during development when DEBUG=True
# SECURITY WARNING: Never enable this in production!
# Serve arquivos de mídia em desenvolvimento quando DEBUG=True
# AVISO DE SEGURANÇA: Nunca habilite isso em produção!
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Optional: Django Debug Toolbar (if installed)
    # Opcional: Django Debug Toolbar (se instalado)
    # try:
    #     import debug_toolbar
    #     urlpatterns = [
    #         path('__debug__/', include(debug_toolbar.urls)),
    #     ] + urlpatterns
    # except ImportError:
    #     pass

# Custom Error Handlers
# Handlers de Erro Customizados

# These handlers are called automatically by Django when errors occur
# They provide custom JSON responses instead of default HTML error pages
#
# Estes handlers são chamados automaticamente pelo Django quando erros ocorrem
# Eles fornecem respostas JSON customizadas ao invés das páginas
# de erro HTML padrão

# 400 Bad Request
handler400 = "core.views.custom_400"

# 403 Forbidden
handler403 = "core.views.custom_403"

# 404 Not Found
handler404 = "core.views.custom_404"

# 500 Internal Server Error
handler500 = "core.views.custom_500"
