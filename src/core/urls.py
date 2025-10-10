"""
URL Configuration - Core Application
Configuração de URLs - Aplicação Core

Defines URL patterns for:
- Authentication views (login, register, logout, profile)
- API endpoints (REST API and custom views)
- Auto-generated ViewSet routes using DRF Router

Define padrões de URL para:
- Views de autenticação (login, registro, logout, perfil)
- Endpoints da API (REST API e views customizadas)
- Rotas de ViewSet auto-geradas usando DRF Router
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views, viewsets

# A router for the API is created to automatically
# generate the URLs for the ViewSets
# Um router para a API é criado para gerar
# automaticamente as URLs para os ViewSets
router = DefaultRouter()

# Register all ViewSets with the router
# Registra todos os ViewSets com o router
router.register(
    r"products", viewsets.ProductViewSet, basename="product"
)  # Product CRUD / CRUD de Produtos
router.register(
    r"categories", viewsets.CategoryViewSet, basename="category"
)  # Category CRUD / CRUD de Categorias
router.register(r"tags", viewsets.TagViewSet, basename="tag")  # Tag CRUD / CRUD de Tags
router.register(
    r"profiles", viewsets.UserProfileViewSet, basename="userprofile"
)  # User Profile CRUD / CRUD de Perfis

urlpatterns = [
    # Authentication URLs / URLs de Autenticação
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("products/", views.products_view, name="products"),
    path("products/create/", views.product_create_view, name="product_create"),
    path("about/", views.about_view, name="about"),
    # API Endpoints / Endpoints da API
    path("api/hello/", views.hello_api, name="hello-api"),
    path("api/info/", views.api_info, name="api-info"),
    # API ViewSets (auto-generated URLs)
    # ViewSets da API (URLs geradas automaticamente)
    path("api/v1/", include(router.urls)),
]
