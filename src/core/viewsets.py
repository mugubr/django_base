# Product ViewSets - Core Application
# ViewSets de Produto - Aplicação Core

# This module defines DRF ViewSets for Product model with:
# - Advanced filtering, searching, and ordering
# - Custom permissions and authentication
# - Pagination configuration
# - Custom actions (endpoints)
# - Performance optimizations
# - Proper error handling
#
# Este módulo define ViewSets DRF para o modelo Product com:
# - Filtragem, busca e ordenação avançadas
# - Permissões e autenticação customizadas
# - Configuração de paginação
# - Ações customizadas (endpoints)
# - Otimizações de performance
# - Tratamento de erros adequado

from datetime import timedelta
from decimal import Decimal

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .models import Product
from .serializers import (
    ProductCreateSerializer,
    ProductListSerializer,
    ProductSerializer,
    ProductUpdateSerializer,
)

# Custom Permissions / Permissões Customizadas


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Authenticated users can do anything.
    Unauthenticated users can only read (GET, HEAD, OPTIONS).

    Permissão customizada: Usuários autenticados podem fazer qualquer coisa.
    Usuários não autenticados podem apenas ler (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        # Read permissions are allowed for any request (even anonymous)
        # Permissões de leitura são permitidas para qualquer requisição (mesmo anônima)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions require authentication
        # Permissões de escrita requerem autenticação
        return request.user and request.user.is_authenticated


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners or admins to edit.
    (For future use when products have owners)

    Permissão em nível de objeto para permitir apenas donos ou admins editarem.
    (Para uso futuro quando produtos tiverem donos)
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        # Permissões de leitura permitidas para qualquer requisição
        if request.method in permissions.SAFE_METHODS:
            return True

        # Admin users have full access
        # Usuários admin têm acesso total
        if request.user and request.user.is_staff:
            return True

        # Future: Check if user owns the product
        # Futuro: Verificar se usuário é dono do produto
        # return obj.owner == request.user

        # For now, allow authenticated users
        # Por enquanto, permite usuários autenticados
        return request.user and request.user.is_authenticated


# Custom Throttle Classes / Classes de Throttle Customizadas


class BurstRateThrottle(UserRateThrottle):
    """
    Burst rate limiting: Prevent rapid-fire requests.
    Limits authenticated users to 10 requests per minute.

    Limitação de taxa de rajada: Previne requisições rápidas em sequência.
    Limita usuários autenticados a 10 requisições por minuto.
    """

    rate = "10/minute"


# Product ViewSet


class ProductViewSet(viewsets.ModelViewSet):
    """
    Comprehensive API endpoint for Product CRUD operations.

    Features:
        - List, Create, Retrieve, Update, Destroy operations
        - Filtering by name, price range, active status
        - Search by name
        - Ordering by any field
        - Pagination (configured globally or per-request)
        - Custom actions: recent, deactivate, activate
        - Permission-based access control
        - Rate limiting

    Endpoint API abrangente para operações CRUD de Product.

    Recursos:
        - Operações List, Create, Retrieve, Update, Destroy
        - Filtragem por nome, faixa de preço, status ativo
        - Busca por nome
        - Ordenação por qualquer campo
        - Paginação (configurada globalmente ou por requisição)
        - Ações customizadas: recent, deactivate, activate
        - Controle de acesso baseado em permissões
        - Limitação de taxa

    Endpoints:
        GET    /api/v1/products/          - List all products
        POST   /api/v1/products/          - Create new product
        GET    /api/v1/products/{id}/     - Retrieve specific product
        PUT    /api/v1/products/{id}/     - Full update
        PATCH  /api/v1/products/{id}/     - Partial update
        DELETE /api/v1/products/{id}/     - Delete product
        GET    /api/v1/products/recent/   - Get recent products (custom action)
        POST   /api/v1/products/{id}/deactivate/ - Deactivate product
        POST   /api/v1/products/{id}/activate/   - Activate product

    Query Parameters:
        ?search=name              - Search by product name
        ?name=value               - Filter by exact name
        ?min_price=10.00          - Filter by minimum price
        ?max_price=100.00         - Filter by maximum price
        ?is_active=true           - Filter by active status
        ?ordering=-created_at     - Order by field (prefix - for descending)
        ?page=1                   - Page number for pagination
        ?page_size=20             - Items per page
    """

    # Basic Configuration / Configuração Básica

    # Base queryset - optimized with select_related/prefetch_related if needed
    # Queryset base - otimizado com select_related/prefetch_related se necessário
    queryset = Product.objects.all().order_by("-created_at")

    # Default serializer (can be overridden per action)
    # Serializador padrão (pode ser sobrescrito por ação)
    serializer_class = ProductSerializer

    # Filtering, Searching, Ordering / Filtragem, Busca, Ordenação

    # Filter backends define how the queryset can be filtered
    # Backends de filtro definem como o queryset pode ser filtrado
    filter_backends = [  # noqa: RUF012
        DjangoFilterBackend,  # Enables field-based filtering
        filters.SearchFilter,  # Enables full-text search
        filters.OrderingFilter,  # Enables result ordering
    ]

    # Fields that can be filtered with exact match
    # Campos que podem ser filtrados com correspondência exata
    filterset_fields = {  # noqa: RUF012
        "name": ["exact", "icontains"],  # name=value or name__icontains=value
        "price": ["exact", "gte", "lte"],  # price__gte=10&price__lte=100
        "is_active": ["exact"],  # is_active=true
        "created_at": ["exact", "gte", "lte"],  # created_at__gte=2024-01-01
    }

    # Fields that can be searched (partial match, case-insensitive)
    # Campos que podem ser buscados (correspondência parcial, case-insensitive)
    search_fields = ["name"]  # ?search=produto  # noqa: RUF012

    # Fields that can be used for ordering results
    # Campos que podem ser usados para ordenar resultados
    ordering_fields = [  # noqa: RUF012
        "name",
        "price",
        "created_at",
        "updated_at",
        "is_active",
    ]

    # Default ordering if not specified in query params
    # Ordenação padrão se não especificada nos parâmetros de query
    ordering = ["-created_at"]  # Newest first / Mais recentes primeiro  # noqa: RUF012

    # -------------------------------------------------------------------------
    # Permissions and Throttling / Permissões e Limitação de Taxa
    # -------------------------------------------------------------------------

    # Permission classes applied to all actions (can be overridden)
    # Classes de permissão aplicadas a todas as ações (pode ser sobrescrito)
    permission_classes = [IsAuthenticatedOrReadOnly]  # noqa: RUF012

    # Throttle classes to prevent API abuse
    # Classes de throttle para prevenir abuso da API
    throttle_classes = [AnonRateThrottle, BurstRateThrottle]  # noqa: RUF012

    # -------------------------------------------------------------------------
    # Dynamic Serializer Selection / Seleção Dinâmica de Serializador
    # -------------------------------------------------------------------------

    def get_serializer_class(self):
        """
        Returns different serializers based on the action.
        This optimizes payload size and improves performance.

        Retorna diferentes serializadores baseados na ação.
        Isso otimiza tamanho do payload e melhora performance.

        Returns:
            Serializer class appropriate for the current action
        """
        # Use lightweight serializer for list view
        # Usa serializador leve para visualização de lista
        if self.action == "list":
            return ProductListSerializer

        # Use specialized serializers for create/update
        # Usa serializadores especializados para criar/atualizar
        if self.action == "create":
            return ProductCreateSerializer

        if self.action in ["update", "partial_update"]:
            return ProductUpdateSerializer

        # Default: full-featured serializer
        # Padrão: serializador completo
        return ProductSerializer

    def get_permissions(self):
        """
        Returns different permissions based on the action.
        Allows fine-grained access control.

        Retorna diferentes permissões baseadas na ação.
        Permite controle de acesso granular.

        Returns:
            List of permission instances
        """
        # Public endpoints - anyone can access
        # Endpoints públicos - qualquer um pode acessar
        if self.action in ["list", "retrieve", "recent"]:
            return [permissions.AllowAny()]

        # Write operations - require authentication
        # Operações de escrita - requerem autenticação
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated()]

        # Administrative actions - require staff privileges
        # Ações administrativas - requerem privilégios de staff
        if self.action in ["deactivate", "activate"]:
            return [permissions.IsAdminUser()]

        # Default: authenticated users only
        # Padrão: apenas usuários autenticados
        return [permissions.IsAuthenticated()]

    # Queryset Optimization / Otimização de Queryset

    def get_queryset(self):
        """
        Returns optimized queryset with custom filters from query parameters.
        Allows advanced filtering beyond standard DjangoFilterBackend.

        Retorna queryset otimizado com filtros customizados dos
        parâmetros de query.
        Permite filtragem avançada além do DjangoFilterBackend padrão.

        Returns:
            Filtered and optimized queryset
        """
        # Start with base queryset
        # Inicia com queryset base
        queryset = super().get_queryset()

        # Custom filter: price range using min_price and max_price params
        # Filtro customizado: faixa de preço usando parâmetros
        # min_price e max_price
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        if min_price:
            try:
                queryset = queryset.filter(price__gte=Decimal(min_price))
            except (ValueError, TypeError):
                pass  # Invalid price value, ignore

        if max_price:
            try:
                queryset = queryset.filter(price__lte=Decimal(max_price))
            except (ValueError, TypeError):
                pass  # Invalid price value, ignore

        # Custom filter: only active products if specified
        # Filtro customizado: apenas produtos ativos se especificado
        active_only = self.request.query_params.get("active_only")
        if active_only and active_only.lower() == "true":
            queryset = queryset.filter(is_active=True)

        # Performance optimization: select_related() for foreign keys
        # Otimização de performance: select_related() para chaves estrangeiras
        # (Not applicable here, but would be used if Product had ForeignKeys)
        # queryset = queryset.select_related('category', 'manufacturer')

        # Performance optimization: prefetch_related() for many-to-many
        # Otimização de performance: prefetch_related() para muitos-para-muitos
        # (Not applicable here, but would be used if Product had M2M fields)
        # queryset = queryset.prefetch_related('tags', 'images')

        return queryset

    # Custom Actions / Ações Customizadas

    @action(detail=False, methods=["get"], url_path="recent")
    def recent(self, request):
        """
        Custom action: Returns products created in the last N days.

        Ação customizada: Retorna produtos criados nos últimos N dias.

        Query Parameters:
            days (int): Number of days to look back (default: 7)

        Example:
            GET /api/v1/products/recent/?days=30

        Returns:
            Response: List of recent products
        """
        # Get days parameter from query params, default to 7
        # Obtém parâmetro days dos query params, padrão 7
        days = int(request.query_params.get("days", 7))

        # Validate days parameter
        # Valida parâmetro days
        if days < 1 or days > 365:
            return Response(
                {
                    "error": "Days must be between 1 and 365. / "
                    "Days deve estar entre 1 e 365."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Calculate cutoff date
        # Calcula data de corte
        cutoff_date = timezone.now() - timedelta(days=days)

        # Filter products
        # Filtra produtos
        recent_products = self.get_queryset().filter(
            created_at__gte=cutoff_date, is_active=True
        )

        # Paginate results
        # Pagina resultados
        page = self.paginate_queryset(recent_products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Serialize and return
        # Serializa e retorna
        serializer = self.get_serializer(recent_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="deactivate")
    def deactivate(self, request, pk=None):
        """
        Custom action: Soft-delete a product by marking it as inactive.

        Ação customizada: Soft-delete de um produto marcando-o como inativo.

        Example:
            POST /api/v1/products/123/deactivate/

        Returns:
            Response: Success message and updated product data
        """
        # Get the product instance
        # Obtém instância do produto
        product = self.get_object()

        # Check if already inactive
        # Verifica se já está inativo
        if not product.is_active:
            return Response(
                {"message": "Product is already inactive. / Produto já está inativo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Deactivate the product
        # Desativa o produto
        product.deactivate()

        # Return success response with updated data
        # Retorna resposta de sucesso com dados atualizados
        serializer = self.get_serializer(product)
        return Response(
            {
                "message": "Product deactivated successfully. / "
                "Produto desativado com sucesso.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="activate")
    def activate(self, request, pk=None):
        """
        Custom action: Reactivate a previously deactivated product.

        Ação customizada: Reativa um produto previamente desativado.

        Example:
            POST /api/v1/products/123/activate/

        Returns:
            Response: Success message and updated product data
        """
        # Get the product instance
        # Obtém instância do produto
        product = self.get_object()

        # Check if already active
        # Verifica se já está ativo
        if product.is_active:
            return Response(
                {"message": "Product is already active. / Produto já está ativo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Activate the product
        # Ativa o produto
        product.activate()

        # Return success response with updated data
        # Retorna resposta de sucesso com dados atualizados
        serializer = self.get_serializer(product)
        return Response(
            {
                "message": "Product activated successfully. / "
                "Produto ativado com sucesso.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"], url_path="price-range")
    def price_range(self, request):
        """
        Custom action: Get products within a specific price range.

        Ação customizada: Obtém produtos dentro de uma faixa
        de preço específica.

        Query Parameters:
            min (Decimal): Minimum price
            max (Decimal): Maximum price

        Example:
            GET /api/v1/products/price-range/?min=10.00&max=100.00

        Returns:
            Response: List of products in price range
        """
        # Get price parameters
        # Obtém parâmetros de preço
        min_price = request.query_params.get("min")
        max_price = request.query_params.get("max")

        # Validate required parameters
        # Valida parâmetros obrigatórios
        if not min_price or not max_price:
            return Response(
                {
                    "error": "Both min and max parameters are required. / "
                    "Ambos parâmetros min e max são obrigatórios."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Convert to Decimal
            # Converte para Decimal
            min_price = Decimal(min_price)
            max_price = Decimal(max_price)

            # Validate range
            # Valida faixa
            if min_price > max_price:
                return Response(
                    {
                        "error": "Minimum price cannot be greater than "
                        "maximum price. / "
                        "Preço mínimo não pode ser maior que preço máximo."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Use model method to get products in range
            # Usa método do modelo para obter produtos na faixa
            products = Product.get_price_range(min_price, max_price)

            # Paginate and return
            # Pagina e retorna
            page = self.paginate_queryset(products)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)

        except (ValueError, TypeError):
            return Response(
                {
                    "error": "Invalid price values. Must be valid decimals. / "
                    "Valores de preço inválidos. Devem ser decimais válidos."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Override Default Methods / Sobrescrever Métodos Padrão

    def perform_create(self, serializer):
        """
        Hook called when creating a new product.
        Can add custom logic like setting the owner.

        Hook chamado ao criar um novo produto.
        Pode adicionar lógica customizada como definir o dono.

        Args:
            serializer: The validated serializer instance
        """
        # Future: Set the product owner to the current user
        # Futuro: Definir o dono do produto como o usuário atual
        # serializer.save(owner=self.request.user)

        # For now, just call parent method
        # Por enquanto, apenas chama método pai
        serializer.save()

    def perform_destroy(self, instance):
        """
        Hook called when deleting a product.
        We override to use soft delete instead of hard delete.

        Hook chamado ao deletar um produto.
        Sobrescrevemos para usar soft delete ao invés de hard delete.

        Args:
            instance: The product instance to delete
        """
        # Soft delete: mark as inactive instead of deleting from DB
        # Soft delete: marca como inativo ao invés de deletar do BD
        instance.deactivate()
