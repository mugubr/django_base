from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views, viewsets

# A router for the API is created to automatically
# generate the URLs for the ViewSets
# Um router para a API é criado para gerar
# automaticamente as URLs para os ViewSets
router = DefaultRouter()

# The 'products' ViewSet is registered with the router.
# O ViewSet 'products' é registrado com o router
router.register(r"products", viewsets.ProductViewSet, basename="product")

urlpatterns = [
    # Function-based view endpoint
    path("hello/", views.hello_api, name="hello-api"),
    # The API URLs are now determined automatically by the router
    # Automaticamente, as URLs da API são determinadas pelo router
    path("", include(router.urls)),
]
