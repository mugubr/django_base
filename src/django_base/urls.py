from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from django_base import settings

urlpatterns = [
    # Django Admin Panel
    # Painel de Administração do Django
    path("admin/", admin.site.urls),
    # Prometheus metrics endpoint
    # Endpoint de métricas do Prometheus
    path("django-metrics/", include("django_prometheus.urls")),
    # Your application's API endpoints
    # Endpoints da API da sua aplicação
    path("api/v1/", include("core.urls")),
]

# Serves media files during development when DEBUG=True
# Serve os arquivos de mídia em desenvolvimento quando DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
