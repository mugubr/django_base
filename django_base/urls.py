from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django Admin Panel
    # Painel de Administração do Django
    path("admin/", admin.site.urls),
    # Prometheus metrics endpoint
    # Endpoint de métricas do Prometheus
    path("prometheus/", include("django_prometheus.urls")),
    # Your application's API endpoints
    # Endpoints da API da sua aplicação
    path("api/v1/", include("core.urls")),
]
