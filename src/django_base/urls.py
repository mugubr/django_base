# Main URL Configuration - Django Base Project
# Configuração Principal de URLs - Projeto Django Base

# This module defines the main URL routing for the entire Django project with:
# - API endpoints (versioned)
# - Admin interface
# - Health check endpoints
# - Metrics endpoints for monitoring
# - API documentation (Swagger/ReDoc)
# - Custom error handlers
# - Static/media file serving (development only)
#
# Este módulo define o roteamento principal de URLs para todo
# o projeto Django com:
# - Endpoints de API (versionados)
# - Interface administrativa
# - Endpoints de health check
# - Endpoints de métricas para monitoramento
# - Documentação da API (Swagger/ReDoc)
# - Handlers de erro customizados
# - Servir arquivos estáticos/mídia (apenas desenvolvimento)

# Import custom error handlers from core app
# Importa handlers de erro customizados da app core
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from core import views
from core.sitemaps import ProductSitemap, StaticViewSitemap
from django_base import settings

# Sitemaps configuration / Configuração de sitemaps
sitemaps = {
    "static": StaticViewSitemap,
    "products": ProductSitemap,
}

# URL Patterns
# Padrões de URL

urlpatterns = [
    # Admin Interface
    # Interface Administrativa
    # Django's built-in admin panel for content management
    # Painel administrativo integrado do Django para gerenciamento de conteúdo
    path("admin/", admin.site.urls),
    # Health Check Endpoints
    # Endpoints de Health Check
    # Used by Docker, Kubernetes, load balancers to monitor application health
    # Usado por Docker, Kubernetes, load balancers para monitorar saúde
    # da aplicação
    path("health/", views.health_check, name="health_check"),
    path("health-status/", views.health_check_page, name="health_status_page"),
    # Monitoring & Metrics
    # Monitoramento & Métricas
    # Prometheus metrics endpoint for application monitoring
    # Endpoint de métricas Prometheus para monitoramento da aplicação
    path("metrics/", include("django_prometheus.urls")),
    # Core Application URLs (includes auth pages and API)
    # URLs da Aplicação Core (inclui páginas de autenticação e API)
    path("", include("core.urls")),
    # API Documentation (drf-spectacular)
    # Documentação da API (drf-spectacular)
    # OpenAPI 3 schema generation
    # Geração de schema OpenAPI 3
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI - Interactive API documentation
    # Swagger UI - Documentação interativa da API
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # ReDoc - Alternative API documentation interface
    # ReDoc - Interface alternativa de documentação da API
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # Sitemap for SEO / Sitemap para SEO
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # JWT Authentication Endpoints / Endpoints de Autenticação JWT
    # Obtain JWT token pair (access + refresh) / Obter par de tokens JWT (acesso + refresh)
    path(
        "api/token/",
        views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    # Refresh access token using refresh token / Renovar token de acesso usando token de refresh
    path(
        "api/token/refresh/",
        views.CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    # Verify token validity / Verificar validade do token
    path(
        "api/token/verify/", views.CustomTokenVerifyView.as_view(), name="token_verify"
    ),
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
