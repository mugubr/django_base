"""
Core Application ViewSets.

This module defines DRF ViewSets for all models in the core application.
Provides comprehensive API endpoints with filtering, searching, ordering,
custom actions, and performance optimizations.

ViewSets da Aplicação Core.

Este módulo define ViewSets DRF para todos os modelos da aplicação core.
Provê endpoints API abrangentes com filtragem, busca, ordenação,
ações customizadas e otimizações de performance.

Classes:
    IsAuthenticatedOrReadOnly: Custom permission class
    IsOwnerOrAdmin: Object-level permission class
    BurstRateThrottle: Rate limiting for burst requests
    ProductViewSet: Complete CRUD for Product model
    CategoryViewSet: Complete CRUD for Category model
    TagViewSet: Complete CRUD for Tag model
    UserProfileViewSet: Complete CRUD for UserProfile model

Features / Recursos:
    - DjangoFilterBackend for field filtering / Filtragem por campo
    - SearchFilter for full-text search / Busca de texto completo
    - OrderingFilter for result ordering / Ordenação de resultados
    - Custom actions with @action decorator / Ações customizadas
    - Permission classes / Classes de permissão
    - Throttling / Limitação de taxa
    - Query optimization / Otimização de queries

Examples / Exemplos:
    # List products / Listar produtos
    GET /api/v1/products/

    # Filter by price range / Filtrar por faixa de preço
    GET /api/v1/products/?price__gte=10&price__lte=100

    # Search by name / Buscar por nome
    GET /api/v1/products/?search=notebook

    # Custom action / Ação customizada
    GET /api/v1/products/recent/?days=7
"""

from datetime import timedelta
from decimal import Decimal

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .models import Category, Product, Tag, UserProfile
from .serializers import (
    CategoryListSerializer,
    CategorySerializer,
    ProductCreateSerializer,
    ProductListSerializer,
    ProductSerializer,
    ProductUpdateSerializer,
    TagListSerializer,
    TagSerializer,
    UserProfileListSerializer,
    UserProfileSerializer,
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
        """
        Check if user has permission for this request.
        Verifica se usuário tem permissão para esta requisição.

        Args / Argumentos:
            request: HTTP request object
            view: View being accessed

        Returns / Retorna:
            bool: True if permission granted
        """
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
        """
        Check if user has permission for this specific object.
        Verifica se usuário tem permissão para este objeto específico.

        Args / Argumentos:
            request: HTTP request object
            view: View being accessed
            obj: Object being accessed

        Returns / Retorna:
            bool: True if permission granted
        """
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
    **English**

    Comprehensive API endpoint for Product CRUD operations.

    ### Features:
    - List, Create, Retrieve, Update, Destroy operations
    - Filtering by name, price range, active status
    - Search by name and ordering by any field
    - Custom actions: `recent`, `deactivate`, `activate`, `price-range`

    ### Endpoints:
    - `GET /api/v1/products/` - List all products
    - `POST /api/v1/products/` - Create a new product
    - `GET /api/v1/products/{id}/` - Retrieve a specific product
    - `PUT/PATCH /api/v1/products/{id}/` - Update a product
    - `DELETE /api/v1/products/{id}/` - Soft-delete a product
    - `GET /api/v1/products/recent/` - Get recent products

    ---
    **Português**

    Endpoint API abrangente para operações CRUD de **Product**.

    ### Recursos:
    - Operações List, Create, Retrieve, Update, Destroy
    - Filtragem por nome, faixa de preço e status de atividade
    - Busca por nome e ordenação por qualquer campo
    - Ações customizadas: `recent`, `deactivate`, `activate`, `price-range`

    ### Endpoints:
    - `GET /api/v1/products/` - Listar todos os produtos
    - `POST /api/v1/products/` - Criar um novo produto
    - `GET /api/v1/products/{id}/` - Detalhar um produto
    - `PUT/PATCH /api/v1/products/{id}/` - Atualizar um produto
    - `DELETE /api/v1/products/{id}/` - Desativar um produto (soft delete)
    - `GET /api/v1/products/recent/` - Obter produtos recentes
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
    filter_backends = [
        DjangoFilterBackend,  # Enables field-based filtering
        filters.SearchFilter,  # Enables full-text search
        filters.OrderingFilter,  # Enables result ordering
    ]

    # Fields that can be filtered with exact match
    # Campos que podem ser filtrados com correspondência exata
    filterset_fields = {
        "name": ["exact", "icontains"],  # name=value or name__icontains=value
        "price": ["exact", "gte", "lte"],  # price__gte=10&price__lte=100
        "is_deleted": ["exact"],  # is_deleted=true
        "created_at": ["exact", "gte", "lte"],  # created_at__gte=2024-01-01
    }

    # Fields that can be searched (partial match, case-insensitive)
    # Campos que podem ser buscados (correspondência parcial, case-insensitive)
    search_fields = ["name"]  # ?search=produto

    # Fields that can be used for ordering results
    # Campos que podem ser usados para ordenar resultados
    ordering_fields = [
        "name",
        "price",
        "created_at",
        "updated_at",
        "is_deleted",
    ]

    # Default ordering if not specified in query params
    # Ordenação padrão se não especificada nos parâmetros de query
    ordering = ["-created_at"]  # Newest first / Mais recentes primeiro

    # Permissions and Throttling / Permissões e Limitação de Taxa

    # Permission classes applied to all actions (can be overridden)
    # Classes de permissão aplicadas a todas as ações (pode ser sobrescrito)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Throttle classes to prevent API abuse
    # Classes de throttle para prevenir abuso da API
    throttle_classes = [AnonRateThrottle, BurstRateThrottle]

    # Dynamic Serializer Selection / Seleção Dinâmica de Serializador

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

        # Performance optimization: select_related() for foreign keys
        # Otimização de performance: select_related() para chaves estrangeiras
        queryset = queryset.select_related("category", "created_by", "updated_by")

        # Performance optimization: prefetch_related() for many-to-many
        # Otimização de performance: prefetch_related() para muitos-para-muitos
        queryset = queryset.prefetch_related("tags")

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
            queryset = queryset.filter(is_deleted=False)

        return queryset

    # Custom Actions / Ações Customizadas

    @action(detail=False, methods=["get"], url_path="recent")
    def recent(self, request):
        """
        **English**

        Get products created in the last N days.

        **Query Parameters:**
        - `days` (int): Number of days to look back (default: 7, min: 1, max: 365)

        **Example Request:**
        ```
        GET /api/v1/products/recent/?days=30
        ```

        **Returns:**
        - 200: Paginated list of recent active products
        - 400: Invalid days parameter

        ---
        **Português**

        Obtém produtos criados nos últimos N dias.

        **Parâmetros de Query:**
        - `days` (int): Número de dias retroativos (padrão: 7, mín: 1, máx: 365)

        **Exemplo de Requisição:**
        ```
        GET /api/v1/products/recent/?days=30
        ```

        **Retorna:**
        - 200: Lista paginada de produtos ativos recentes
        - 400: Parâmetro days inválido
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
            created_at__gte=cutoff_date, is_deleted=False
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
        **English**

        Soft-delete a product by marking it as inactive.

        **Example Request:**
        ```
        POST /api/v1/products/123/deactivate/
        ```

        **Returns:**
        - 200: Product deactivated successfully with updated data
        - 400: Product is already inactive
        - 404: Product not found

        ---
        **Português**

        Soft-delete de um produto marcando-o como inativo.

        **Exemplo de Requisição:**
        ```
        POST /api/v1/products/123/deactivate/
        ```

        **Retorna:**
        - 200: Produto desativado com sucesso com dados atualizados
        - 400: Produto já está inativo
        - 404: Produto não encontrado
        """
        # Get the product instance
        # Obtém instância do produto
        product = self.get_object()

        # Check if already inactive
        # Verifica se já está inativo
        if not not product.is_deleted:
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
        **English**

        Reactivate a previously deactivated product.

        **Example Request:**
        ```
        POST /api/v1/products/123/activate/
        ```

        **Returns:**
        - 200: Product activated successfully with updated data
        - 400: Product is already active
        - 404: Product not found

        ---
        **Português**

        Reativa um produto previamente desativado.

        **Exemplo de Requisição:**
        ```
        POST /api/v1/products/123/activate/
        ```

        **Retorna:**
        - 200: Produto ativado com sucesso com dados atualizados
        - 400: Produto já está ativo
        - 404: Produto não encontrado
        """
        # Get the product instance
        # Obtém instância do produto
        product = self.get_object()

        # Check if already active
        # Verifica se já está ativo
        if not product.is_deleted:
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
        **English**

        Get products within a specific price range.

        **Query Parameters:**
        - `min` (Decimal, required): Minimum price
        - `max` (Decimal, required): Maximum price

        **Example Request:**
        ```
        GET /api/v1/products/price-range/?min=10.00&max=100.00
        ```

        **Returns:**
        - 200: Paginated list of products in price range
        - 400: Missing or invalid parameters, or min > max

        ---
        **Português**

        Obtém produtos dentro de uma faixa de preço específica.

        **Parâmetros de Query:**
        - `min` (Decimal, obrigatório): Preço mínimo
        - `max` (Decimal, obrigatório): Preço máximo

        **Exemplo de Requisição:**
        ```
        GET /api/v1/products/price-range/?min=10.00&max=100.00
        ```

        **Retorna:**
        - 200: Lista paginada de produtos na faixa de preço
        - 400: Parâmetros ausentes ou inválidos, ou min > max
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
        # Soft delete: mark as deleted instead of deleting from DB
        # Soft delete: marca como deletado ao invés de deletar do BD
        instance.soft_delete()


# Category ViewSet


class CategoryViewSet(viewsets.ModelViewSet):
    """
    **English**

    API endpoint for Category CRUD operations.

    ### Features:
    - Hierarchical category management
    - Filtering, searching, and ordering
    - Product count per category
    - Custom action for tree navigation (`/tree/`)

    ### Endpoints:
    - `GET /api/v1/categories/` - List all categories
    - `POST /api/v1/categories/` - Create a new category
    - `GET /api/v1/categories/tree/` - Get the complete category hierarchy

    ---
    **Português**

    Endpoint API para operações CRUD de **Category**.

    ### Recursos:
    - Gerenciamento hierárquico de categorias
    - Filtragem, busca e ordenação
    - Contagem de produtos por categoria
    - Ação customizada para navegação em árvore (`/tree/`)

    ### Endpoints:
    - `GET /api/v1/categories/` - Listar todas as categorias
    - `POST /api/v1/categories/` - Criar uma nova categoria
    - `GET /api/v1/categories/tree/` - Obter a hierarquia de categorias em árvore
    """

    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = {
        "name": ["exact", "icontains"],
        "is_deleted": ["exact"],
        "parent": ["exact", "isnull"],  # parent__isnull=true for root categories
    }

    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

    def get_serializer_class(self):
        """
        Use lightweight serializer for list view.
        Usa serializador leve para visualização de lista.

        Returns / Retorna:
            Serializer class: Appropriate serializer for action
        """
        if self.action == "list":
            return CategoryListSerializer
        return CategorySerializer

    def get_queryset(self):
        """
        Optimize queryset with select_related for parent.
        Prevents N+1 queries by prefetching related objects.

        Otimiza queryset com select_related para parent.
        Previne queries N+1 ao buscar objetos relacionados previamente.

        Returns / Retorna:
            QuerySet: Optimized category queryset
        """
        queryset = super().get_queryset()
        queryset = queryset.select_related("parent", "created_by", "updated_by")
        queryset = queryset.prefetch_related("children")
        return queryset

    @action(detail=False, methods=["get"], url_path="tree")
    def tree(self, request):
        """
        **English**

        Get complete category hierarchy as a nested tree structure.

        **Example Request:**
        ```
        GET /api/v1/categories/tree/
        ```

        **Returns:**
        - 200: Nested category tree with children (only active categories)

        ---
        **Português**

        Obtém hierarquia completa de categorias como estrutura de árvore aninhada.

        **Exemplo de Requisição:**
        ```
        GET /api/v1/categories/tree/
        ```

        **Retorna:**
        - 200: Árvore de categorias aninhada com filhos (apenas categorias ativas)
        """
        # Get only root categories (no parent)
        # Obtém apenas categorias raiz (sem pai)
        root_categories = self.get_queryset().filter(
            parent__isnull=True, is_deleted=False
        )

        def build_tree(category):
            """
            Recursively build category tree.
            Constrói árvore de categorias recursivamente.

            Args / Argumentos:
                category: Root category instance

            Returns / Retorna:
                dict: Nested category data
            """
            data = CategorySerializer(category).data
            children = category.children.filter(is_deleted=False)
            if children.exists():
                data["children"] = [build_tree(child) for child in children]
            return data

        tree_data = [build_tree(cat) for cat in root_categories]
        return Response(tree_data)


# Tag ViewSet


class TagViewSet(viewsets.ModelViewSet):
    """
    **English**

    API endpoint for Tag CRUD operations.

    ### Features:
    - Tag management with color support
    - Filtering, searching, and ordering
    - Product count per tag
    - Custom action for popular tags (`/popular/`)

    ### Endpoints:
    - `GET /api/v1/tags/` - List all tags
    - `POST /api/v1/tags/` - Create a new tag
    - `GET /api/v1/tags/popular/` - Get the most used tags

    ---
    **Português**

    Endpoint API para operações CRUD de **Tag**.

    ### Recursos:
    - Gerenciamento de tags com suporte a cores
    - Filtragem, busca e ordenação
    - Contagem de produtos por tag
    - Ação customizada para listar as tags mais populares (`/popular/`)

    ### Endpoints:
    - `GET /api/v1/tags/` - Listar todas as tags
    - `POST /api/v1/tags/` - Criar uma nova tag
    - `GET /api/v1/tags/popular/` - Obter as tags mais utilizadas
    """

    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = {"name": ["exact", "icontains"], "color": ["exact"]}
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

    def get_serializer_class(self):
        """
        Use lightweight serializer for list view.
        Usa serializador leve para visualização de lista.

        Returns / Retorna:
            Serializer class: Appropriate serializer for action
        """
        if self.action == "list":
            return TagListSerializer
        return TagSerializer

    def get_queryset(self):
        """
        Optimize queryset with select_related for created_by.
        Prevents N+1 queries on foreign key relationship.

        Otimiza queryset com select_related para created_by.
        Previne queries N+1 em relacionamento de chave estrangeira.

        Returns / Retorna:
            QuerySet: Optimized tag queryset
        """
        queryset = super().get_queryset()
        queryset = queryset.select_related("created_by")
        return queryset

    @action(detail=False, methods=["get"], url_path="popular")
    def popular(self, request):
        """
        **English**

        Get most popular tags ordered by product count.

        **Query Parameters:**
        - `limit` (int): Number of tags to return (default: 10)

        **Example Request:**
        ```
        GET /api/v1/tags/popular/?limit=20
        ```

        **Returns:**
        - 200: List of popular tags with product_count annotation

        ---
        **Português**

        Obtém tags mais populares ordenadas por contagem de produtos.

        **Parâmetros de Query:**
        - `limit` (int): Número de tags a retornar (padrão: 10)

        **Exemplo de Requisição:**
        ```
        GET /api/v1/tags/popular/?limit=20
        ```

        **Retorna:**
        - 200: Lista de tags populares com anotação product_count
        """
        from django.db.models import Count

        limit = int(request.query_params.get("limit", 10))

        # Annotate tags with product count and order by it
        # Anota tags com contagem de produtos e ordena por isso
        popular_tags = (
            self.get_queryset()
            .annotate(product_count=Count("products"))
            .filter(product_count__gt=0)
            .order_by("-product_count")[:limit]
        )

        serializer = self.get_serializer(popular_tags, many=True)
        return Response(serializer.data)


# UserProfile ViewSet


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    **English**

    API endpoint for UserProfile operations.

    ### Features:
    - User profile management
    - Avatar upload support
    - Filtering, searching, and ordering
    - Special endpoint (`/me/`) for the logged-in user's profile

    ### Endpoints:
    - `GET /api/v1/profiles/` - List all profiles
    - `GET /api/v1/profiles/me/` - View/Edit **your own** profile
    - `GET /api/v1/profiles/{id}/` - Retrieve a specific profile

    ---
    **Português**

    Endpoint API para operações de **UserProfile**.

    ### Recursos:
    - Gerenciamento de perfis de usuário
    - Suporte a upload de avatar
    - Filtragem, busca e ordenação
    - Endpoint especial (`/me/`) para o perfil do usuário logado

    ### Endpoints:
    - `GET /api/v1/profiles/` - Listar todos os perfis
    - `GET /api/v1/profiles/me/` - Visualizar/editar o **seu** perfil
    - `GET /api/v1/profiles/{id}/` - Detalhar um perfil específico
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = {
        "is_verified": ["exact"],
        "city": ["exact", "icontains"],
        "country": ["exact", "icontains"],
    }

    search_fields = ["user__username", "user__email", "bio", "city"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        """
        Use lightweight serializer for list view.
        Usa serializador leve para visualização de lista.

        Returns / Retorna:
            Serializer class: Appropriate serializer for action
        """
        if self.action == "list":
            return UserProfileListSerializer
        return UserProfileSerializer

    def get_queryset(self):
        """
        Optimize queryset with select_related for user.
        Prevents N+1 queries on foreign key relationship.

        Otimiza queryset com select_related para user.
        Previne queries N+1 em relacionamento de chave estrangeira.

        Returns / Retorna:
            QuerySet: Optimized profile queryset
        """
        queryset = super().get_queryset()
        queryset = queryset.select_related("user")
        return queryset

    def get_permissions(self):
        """
        Custom permissions: users can only edit their own profile.
        Permissões customizadas: usuários podem apenas editar seu próprio perfil.

        Returns / Retorna:
            list: Permission instances for current action
        """
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]

        if self.action in ["update", "partial_update"]:
            return [permissions.IsAuthenticated()]

        if self.action == "me":
            return [permissions.IsAuthenticated()]

        return [permissions.IsAdminUser()]

    @action(detail=False, methods=["get", "put", "patch"], url_path="me")
    def me(self, request):
        """
        **English**

        Get or update the authenticated user's profile.

        **Methods:**
        - `GET`: Retrieve your profile
        - `PUT`: Full update of your profile
        - `PATCH`: Partial update of your profile

        **Example Requests:**
        ```
        GET   /api/v1/profiles/me/
        PUT   /api/v1/profiles/me/
        PATCH /api/v1/profiles/me/
        ```

        **Returns:**
        - 200: Profile data (GET) or updated profile data (PUT/PATCH)
        - 400: Validation errors (PUT/PATCH)
        - 401: Authentication required

        ---
        **Português**

        Obtém ou atualiza o perfil do usuário autenticado.

        **Métodos:**
        - `GET`: Recuperar seu perfil
        - `PUT`: Atualização completa do seu perfil
        - `PATCH`: Atualização parcial do seu perfil

        **Exemplos de Requisição:**
        ```
        GET   /api/v1/profiles/me/
        PUT   /api/v1/profiles/me/
        PATCH /api/v1/profiles/me/
        ```

        **Retorna:**
        - 200: Dados do perfil (GET) ou dados do perfil atualizado (PUT/PATCH)
        - 400: Erros de validação (PUT/PATCH)
        - 401: Autenticação requerida
        """
        # Get current user's profile
        # Obtém perfil do usuário atual
        profile = request.user.profile

        if request.method == "GET":
            serializer = self.get_serializer(profile)
            return Response(serializer.data)

        elif request.method in ["PUT", "PATCH"]:
            partial = request.method == "PATCH"
            serializer = self.get_serializer(
                profile, data=request.data, partial=partial
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
