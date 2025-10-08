"""
Core Application Serializers.

This module defines DRF serializers for all models in the core application.
Provides comprehensive validation, computed fields, and specialized serializers
for different use cases.

Serializadores da Aplicação Core.

Este módulo define serializadores DRF para todos os modelos da aplicação core.
Provê validação abrangente, campos computados e serializadores especializados
para diferentes casos de uso.

Classes:
    ProductListSerializer: Lightweight serializer for product listings
    ProductSerializer: Full-featured product serializer with validation
    ProductCreateSerializer: Specialized serializer for product creation
    ProductUpdateSerializer: Specialized serializer for product updates
    CategorySerializer: Full category serializer with hierarchy support
    CategoryListSerializer: Lightweight category list serializer
    TagSerializer: Full tag serializer with color validation
    TagListSerializer: Lightweight tag list serializer
    UserProfileSerializer: Full user profile serializer
    UserProfileListSerializer: Lightweight profile list serializer

Features / Recursos:
    - Field-level validation / Validação em nível de campo
    - Object-level validation / Validação em nível de objeto
    - Computed read-only fields / Campos computados somente-leitura
    - Custom error messages (bilingual) / Mensagens de erro customizadas (bilíngue)
    - Performance optimizations / Otimizações de performance

Examples / Exemplos:
    # Create a product / Criar um produto
    serializer = ProductCreateSerializer(data={'name': 'Test', 'price': '10.00'})
    if serializer.is_valid():
        product = serializer.save()

    # List products / Listar produtos
    products = Product.objects.all()
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)
"""

from decimal import Decimal

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Category, Product, Tag, UserProfile


class ProductListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for product listings.
    Only includes essential fields to minimize payload size
    and improve performance.

    Serializador leve para listagens de produtos.
    Inclui apenas campos essenciais para minimizar tamanho do
    payload e melhorar performance.

    Fields:
        - id: Product unique identifier
        - name: Product name
        - price: Product price
        - is_active: Active status

    Use Cases:
        - GET /api/v1/products/ (list view)
        - Dropdowns and autocomplete widgets
        - Mobile apps with limited bandwidth
    """

    class Meta:
        """
        Meta configuration for ProductListSerializer.
        Defines model, fields, and read-only constraints.

        Configuração Meta para ProductListSerializer.
        Define modelo, campos e restrições de somente-leitura.

        Attributes / Atributos:
            model: Product model class
            fields: Minimal field set for list view (id, name, price, is_active)
            read_only_fields: Fields that cannot be modified (id)
        """

        model = Product
        fields = ["id", "name", "price", "is_active"]  # noqa: RUF012
        read_only_fields = ["id"]  # noqa: RUF012


class ProductSerializer(serializers.ModelSerializer):
    """
    Full-featured serializer for Product model with comprehensive validation.
    Includes computed fields and custom validation logic.

    Serializador completo para o modelo Product com validação abrangente.
    Inclui campos computados e lógica de validação customizada.

    Fields:
        - id: Product unique identifier (read-only)
        - name: Product name (validated)
        - price: Product price (validated)
        - created_at: Creation timestamp (read-only)
        - updated_at: Last update timestamp (read-only)
        - is_active: Active status
        - is_new: Computed field indicating if product is new (read-only)
        - formatted_price: Formatted price with currency (read-only)
        - age_in_days: Days since creation (read-only)

    Validations:
        - Name: minimum 3 characters, no whitespace-only
        - Price: must be positive, maximum value enforced
    """

    # Computed Read-Only Fields / Campos Computados Somente-Leitura

    # Uses the @property method from the model
    # Usa o método @property do modelo
    is_new = serializers.BooleanField(read_only=True)

    # Uses SerializerMethodField for custom formatting
    # Usa SerializerMethodField para formatação customizada
    formatted_price = serializers.SerializerMethodField()

    # Another computed field from model property
    # Outro campo computado da propriedade do modelo
    age_in_days = serializers.IntegerField(read_only=True)

    class Meta:
        """
        Meta configuration for ProductSerializer.
        Defines comprehensive field set including computed fields.

        Configuração Meta para ProductSerializer.
        Define conjunto abrangente de campos incluindo campos computados.

        Attributes / Atributos:
            model: Product model class
            fields: Complete field set including computed fields
            read_only_fields: Auto-generated and computed fields
        """

        model = Product
        fields = [  # noqa: RUF012
            "id",
            "name",
            "price",
            "formatted_price",  # Computed field / Campo computado
            "created_at",
            "updated_at",
            "is_active",
            "is_new",  # Computed field / Campo computado
            "age_in_days",  # Computed field / Campo computado
        ]
        read_only_fields = [  # noqa: RUF012
            "id",
            "created_at",
            "updated_at",
            "is_new",
            "formatted_price",
            "age_in_days",
        ]

    # Field-Level Validations / Validações em Nível de Campo

    def validate_name(self, value):
        """
        Validates the product name field.

        Rules:
            - Cannot be empty or whitespace-only
            - Must have at least 3 characters after trimming
            - Trailing/leading spaces are automatically removed

        Valida o campo nome do produto.

        Regras:
            - Não pode ser vazio ou conter apenas espaços
            - Deve ter pelo menos 3 caracteres após remoção de espaços
            - Espaços no início/fim são removidos automaticamente

        Args:
            value (str): The product name to validate

        Returns:
            str: Cleaned and validated name

        Raises:
            serializers.ValidationError: If validation fails
        """
        # Strip whitespace for validation
        # Remove espaços para validação
        cleaned_value = value.strip() if value else ""

        # Check if name is empty after stripping
        # Verifica se nome está vazio após remoção de espaços
        if not cleaned_value:
            raise serializers.ValidationError(
                "Product name cannot be empty "
                "or whitespace only. / "
                "O nome do produto não pode ser "
                "vazio ou conter apenas espaços."
            )

        # Check minimum length
        # Verifica comprimento mínimo
        if len(cleaned_value) < 3:
            raise serializers.ValidationError(
                "Product name must have at least 3 characters. / "
                "O nome do produto deve ter pelo menos 3 caracteres."
            )

        # Check maximum length (redundant with CharField max_length
        # but explicit)
        # Verifica comprimento máximo (redundante com max_length do CharField
        # mas explícito)
        if len(cleaned_value) > 100:
            raise serializers.ValidationError(
                "Product name cannot exceed 100 characters. / "
                "O nome do produto não pode exceder 100 caracteres."
            )

        # Return cleaned value
        # Retorna valor limpo
        return cleaned_value

    def validate_price(self, value):
        """
        Validates the product price field.

        Rules:
            - Must be greater than zero
            - Cannot exceed maximum value (9,999,999.99)
            - Must have exactly 2 decimal places

        Valida o campo preço do produto.

        Regras:
            - Deve ser maior que zero
            - Não pode exceder valor máximo (9.999.999,99)
            - Deve ter exatamente 2 casas decimais

        Args:
            value (Decimal): The price to validate

        Returns:
            Decimal: Validated price

        Raises:
            serializers.ValidationError: If validation fails
        """
        # Check if price is positive
        # Verifica se preço é positivo
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero. / O preço deve ser maior que zero."
            )

        # Check maximum price
        # Verifica preço máximo
        max_price = Decimal("9999999.99")
        if value > max_price:
            raise serializers.ValidationError(
                f"Price cannot exceed {max_price}. / "
                f"O preço não pode exceder {max_price}."
            )

        # Check minimum price (e.g., prevent prices like 0.01)
        # Verifica preço mínimo (ex: previne preços como 0.01)
        min_price = Decimal("0.01")
        if value < min_price:
            raise serializers.ValidationError(
                f"Price must be at least {min_price}. / "
                f"O preço deve ser pelo menos {min_price}."
            )

        return value

    # Object-Level Validations / Validações em Nível de Objeto

    def validate(self, attrs):
        """
        Object-level validation for cross-field validation logic.
        Called after all field-level validations pass.

        Validação em nível de objeto para lógica de validação entre campos.
        Chamada após todas as validações em nível de campo passarem.

        Args:
            attrs (dict): Dictionary of validated field values

        Returns:
            dict: Validated attributes

        Raises:
            serializers.ValidationError: If cross-field validation fails
        """
        # Example: Could add business logic like:
        # - If price > 1000, require special approval field
        # - Prevent duplicate names for active products
        # - Apply seasonal pricing rules
        #
        # Exemplo: Poderia adicionar lógica de negócio como:
        # - Se preço > 1000, requerer campo de aprovação especial
        # - Prevenir nomes duplicados para produtos ativos
        # - Aplicar regras de preço sazonal

        # Example validation: warn if creating expensive product
        # Validação de exemplo: avisar se criando produto caro
        price = attrs.get("price")
        if price and price > Decimal("10000"):
            # This is just a warning - you could make it an error
            # Este é apenas um aviso - você poderia torná-lo um erro
            # For now, we'll allow it but could log it
            # Por enquanto, vamos permitir mas poderíamos logar
            pass

        return attrs

    # Custom Methods / Métodos Customizados
    @extend_schema_field(serializers.CharField)
    def get_formatted_price(self, obj):
        """
        Returns formatted price with currency symbol.
        Uses the model's property method.

        Retorna preço formatado com símbolo de moeda.
        Usa o método property do modelo.

        Args:
            obj (Product): Product instance

        Returns:
            str: Formatted price (e.g., "R$ 99.99")
        """
        return obj.formatted_price

    # Custom Create/Update Methods / Métodos Create/Update Customizados

    def create(self, validated_data):
        """
        Custom create method with additional logging/processing.
        Called when creating a new product via API.

        Método create customizado com logging/processamento adicional.
        Chamado ao criar um novo produto via API.

        Args:
            validated_data (dict): Validated data from serializer

        Returns:
            Product: Created product instance
        """
        # You could add custom logic here, such as:
        # - Logging the creation
        # - Sending notifications
        # - Updating related models
        #
        # Você poderia adicionar lógica customizada aqui, como:
        # - Logar a criação
        # - Enviar notificações
        # - Atualizar modelos relacionados

        # Call parent create method
        # Chama método create da classe pai
        product = super().create(validated_data)

        # Additional processing could go here
        # Processamento adicional poderia ir aqui

        return product

    def update(self, instance, validated_data):
        """
        Custom update method with change tracking.
        Called when updating an existing product via API.

        Método update customizado com rastreamento de mudanças.
        Chamado ao atualizar um produto existente via API.

        Args:
            instance (Product): Existing product instance
            validated_data (dict): New validated data

        Returns:
            Product: Updated product instance
        """
        # Track price changes for audit log
        # Rastreia mudanças de preço para log de auditoria
        old_price = instance.price
        new_price = validated_data.get("price", old_price)

        if old_price != new_price:
            # Here you could:
            # - Log the price change
            # - Send notification to admins
            # - Create audit trail entry
            #
            # Aqui você poderia:
            # - Logar a mudança de preço
            # - Enviar notificação para admins
            # - Criar entrada de trilha de auditoria
            pass

        # Call parent update method
        # Chama método update da classe pai
        return super().update(instance, validated_data)


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Specialized serializer for product creation.
    May have different validation rules or required fields than update.

    Serializador especializado para criação de produtos.
    Pode ter regras de validação ou campos obrigatórios diferentes
    da atualização.

    Use Cases:
        - POST /api/v1/products/
        - Bulk import operations
        - Admin product creation
    """

    class Meta:
        """
        Meta configuration for ProductCreateSerializer.
        Enforces required fields for product creation.

        Configuração Meta para ProductCreateSerializer.
        Impõe campos obrigatórios para criação de produtos.

        Attributes / Atributos:
            model: Product model class
            fields: Fields allowed during creation
            extra_kwargs: Field-specific requirements and defaults
        """

        model = Product
        fields = ["name", "price", "is_active"]  # noqa: RUF012
        # All fields are required on creation / Todos os campos são obrigatórios na criação
        extra_kwargs = {  # noqa: RUF012
            "name": {"required": True},
            "price": {"required": True},
            "is_active": {"required": False, "default": True},
        }


class ProductUpdateSerializer(serializers.ModelSerializer):
    """
    Specialized serializer for product updates.
    All fields are optional - only update what's provided.

    Serializador especializado para atualizações de produtos.
    Todos os campos são opcionais - atualiza apenas o que for fornecido.

    Use Cases:
        - PUT/PATCH /api/v1/products/{id}/
        - Partial updates
        - Bulk updates
    """

    class Meta:
        """
        Meta configuration for ProductUpdateSerializer.
        All fields are optional for partial updates.

        Configuração Meta para ProductUpdateSerializer.
        Todos os campos são opcionais para atualizações parciais.

        Attributes / Atributos:
            model: Product model class
            fields: Fields that can be updated
            extra_kwargs: All fields are optional (supports PATCH)
        """

        model = Product
        fields = ["name", "price", "is_active"]  # noqa: RUF012
        # All fields optional for partial updates / Todos os campos opcionais para atualizações parciais
        extra_kwargs = {  # noqa: RUF012
            "name": {"required": False},
            "price": {"required": False},
            "is_active": {"required": False},
        }


# Category Serializers / Serializadores de Categoria


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model with hierarchical support.
    Serializador para o modelo Category com suporte hierárquico.

    Fields:
        - id: Category unique identifier (read-only)
        - name: Category name
        - slug: URL-friendly slug (auto-generated if not provided)
        - description: Category description
        - parent: Parent category ID (for hierarchical categories)
        - parent_name: Parent category name (read-only)
        - children_count: Number of child categories (read-only)
        - products_count: Number of products in category (read-only)
        - is_active: Active status
    """

    parent_name = serializers.SerializerMethodField()
    children_count = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()

    class Meta:
        """
        Meta configuration for CategorySerializer.
        Supports hierarchical category structure.

        Configuração Meta para CategorySerializer.
        Suporta estrutura hierárquica de categorias.

        Attributes / Atributos:
            model: Category model class
            fields: Complete field set including hierarchy and counts
            read_only_fields: Auto-generated fields (id, slug, timestamps)
        """

        model = Category
        fields = [  # noqa: RUF012
            "id",
            "name",
            "slug",
            "description",
            "parent",
            "parent_name",
            "children_count",
            "products_count",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]  # noqa: RUF012

    @extend_schema_field(serializers.CharField)
    def get_parent_name(self, obj):
        """
        Returns parent category name or None.
        Retorna nome da categoria pai ou None.

        Args / Argumentos:
            obj: Category instance

        Returns / Retorna:
            str or None: Parent category name
        """
        return obj.parent.name if obj.parent else None

    @extend_schema_field(serializers.IntegerField)
    def get_children_count(self, obj):
        """
        Returns number of child categories.
        Retorna número de categorias filhas.

        Args / Argumentos:
            obj: Category instance

        Returns / Retorna:
            int: Count of child categories
        """
        return obj.children.count()

    @extend_schema_field(serializers.IntegerField)
    def get_products_count(self, obj):
        """
        Returns number of active products in this category.
        Retorna número de produtos ativos nesta categoria.

        Args / Argumentos:
            obj: Category instance

        Returns / Retorna:
            int: Count of active products
        """
        return obj.products.filter(is_active=True).count()

    def validate_parent(self, value):
        """
        Prevent circular references in category hierarchy.
        Previne referências circulares na hierarquia de categorias.

        Args / Argumentos:
            value: Parent category instance

        Returns / Retorna:
            Category: Validated parent category

        Raises / Lança:
            ValidationError: If circular reference detected
        """
        if value and self.instance:
            # Check if parent is the same as current category
            if value.id == self.instance.id:
                raise serializers.ValidationError(
                    "Category cannot be its own parent. / "
                    "Categoria não pode ser seu próprio pai."
                )

            # Check if parent is a child of current category
            if value.parent and value.parent.id == self.instance.id:
                raise serializers.ValidationError(
                    "Circular reference detected. / Referência circular detectada."
                )

        return value


class CategoryListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for category listings.
    Serializador leve para listagens de categorias.

    Fields / Campos:
        id: Category ID (read-only)
        name: Category name
        slug: URL-friendly slug (read-only)
        is_active: Active status
        products_count: Number of active products (computed)
    """

    products_count = serializers.SerializerMethodField()

    class Meta:
        """
        Meta configuration for CategoryListSerializer.
        Configuração Meta para CategoryListSerializer.
        """

        model = Category
        fields = ["id", "name", "slug", "is_active", "products_count"]  # noqa: RUF012
        read_only_fields = ["id", "slug"]  # noqa: RUF012

    @extend_schema_field(serializers.IntegerField)
    def get_products_count(self, obj):
        """
        Returns count of active products.
        Retorna contagem de produtos ativos.
        """
        return obj.products.filter(is_active=True).count()


# Tag Serializers / Serializadores de Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model with color support.
    Serializador para o modelo Tag com suporte a cores.

    Fields:
        - id: Tag unique identifier (read-only)
        - name: Tag name
        - slug: URL-friendly slug (auto-generated if not provided)
        - color: Hex color code for UI display
        - products_count: Number of products with this tag (read-only)
    """

    products_count = serializers.SerializerMethodField()

    class Meta:
        """
        Meta configuration for TagSerializer.
        Configuração Meta para TagSerializer.

        Attributes / Atributos:
            model: Tag model class
            fields: All tag fields including computed products_count
            read_only_fields: Auto-generated fields
        """

        model = Tag
        fields = [  # noqa: RUF012
            "id",
            "name",
            "slug",
            "color",
            "products_count",
            "created_at",
        ]
        read_only_fields = ["id", "slug", "created_at"]  # noqa: RUF012

    @extend_schema_field(serializers.IntegerField)
    def get_products_count(self, obj):
        """
        Returns number of active products with this tag.
        Retorna número de produtos ativos com esta tag.

        Args / Argumentos:
            obj: Tag instance

        Returns / Retorna:
            int: Count of active products
        """
        return obj.products.filter(is_active=True).count()

    def validate_color(self, value):
        """
        Validate hex color format (#RRGGBB).
        Valida formato de cor hexadecimal (#RRGGBB).

        Args / Argumentos:
            value (str): Hex color code

        Returns / Retorna:
            str: Validated and normalized color (uppercase)

        Raises / Lança:
            ValidationError: If color format is invalid
        """
        import re

        if not re.match(r"^#[0-9A-Fa-f]{6}$", value):
            raise serializers.ValidationError(
                "Color must be in hex format (#RRGGBB). / "
                "Cor deve estar em formato hex (#RRGGBB)."
            )
        return value.upper()  # Normalize to uppercase


class TagListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for tag listings.
    Serializador leve para listagens de tags.

    Fields / Campos:
        id: Tag ID (read-only)
        name: Tag name
        slug: URL-friendly slug (read-only)
        color: Hex color code for display
    """

    class Meta:
        """
        Meta configuration for TagListSerializer.
        Configuração Meta para TagListSerializer.
        """

        model = Tag
        fields = ["id", "name", "slug", "color"]  # noqa: RUF012
        read_only_fields = ["id", "slug"]  # noqa: RUF012


# UserProfile Serializers / Serializadores de UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model.
    Serializador para o modelo UserProfile.

    Fields:
        - user: User ID (read-only on update)
        - username: Username from related User (read-only)
        - email: Email from related User (read-only)
        - full_name: Full name from related User (read-only)
        - bio: User biography
        - avatar: Profile picture
        - phone: Phone number
        - birth_date: Birth date
        - city: City
        - country: Country
        - website: Website URL
        - is_verified: Verification status (read-only)
    """

    # Related User fields
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        """
        Meta configuration for UserProfileSerializer.
        Configuração Meta para UserProfileSerializer.

        Attributes / Atributos:
            model: UserProfile model class
            fields: Complete profile fields including related User fields
            read_only_fields: Auto-generated and system fields
        """

        model = UserProfile
        fields = [  # noqa: RUF012
            "id",
            "user",
            "username",
            "email",
            "full_name",
            "bio",
            "avatar",
            "phone",
            "birth_date",
            "city",
            "country",
            "website",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [  # noqa: RUF012
            "id",
            "user",
            "is_verified",
            "created_at",
            "updated_at",
        ]

    @extend_schema_field(serializers.CharField)
    def get_full_name(self, obj):
        """
        Returns user's full name or username as fallback.
        Retorna nome completo do usuário ou username como fallback.

        Args / Argumentos:
            obj: UserProfile instance

        Returns / Retorna:
            str: User's full name or username
        """
        return obj.user.get_full_name() or obj.user.username

    def validate_phone(self, value):
        """
        Basic phone number validation.
        Validates that phone contains only digits and optional + prefix.

        Validação básica de número de telefone.
        Valida que telefone contém apenas dígitos e prefixo + opcional.

        Args / Argumentos:
            value (str): Phone number to validate

        Returns / Retorna:
            str: Validated phone number

        Raises / Lança:
            ValidationError: If phone format is invalid
        """
        if value:
            # Remove common formatting characters
            cleaned = (
                value.replace(" ", "")
                .replace("-", "")
                .replace("(", "")
                .replace(")", "")
            )
            if not cleaned.replace("+", "").isdigit():
                raise serializers.ValidationError(
                    "Phone number must contain only digits and optional + prefix. / "
                    "Número de telefone deve conter apenas dígitos e prefixo + opcional."
                )
        return value

    def validate_website(self, value):
        """
        Ensure website URL is valid and uses http/https protocol.
        Garante que URL do website é válida e usa protocolo http/https.

        Args / Argumentos:
            value (str): Website URL to validate

        Returns / Retorna:
            str: Validated website URL

        Raises / Lança:
            ValidationError: If URL doesn't start with http:// or https://
        """
        if value and not value.startswith(("http://", "https://")):
            raise serializers.ValidationError(
                "Website URL must start with http:// or https://. / "
                "URL do website deve começar com http:// ou https://."
            )
        return value


class UserProfileListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for user profile listings.
    Serializador leve para listagens de perfis de usuário.

    Fields / Campos:
        id: Profile ID (read-only)
        user: User ID (read-only)
        username: Username from related User (read-only)
        full_name: Computed full name (read-only)
        avatar: Profile picture
        city: User's city
        country: User's country
        is_verified: Verification status (read-only)
    """

    username = serializers.CharField(source="user.username", read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        """
        Meta configuration for UserProfileListSerializer.
        Configuração Meta para UserProfileListSerializer.
        """

        model = UserProfile
        fields = [  # noqa: RUF012
            "id",
            "user",
            "username",
            "full_name",
            "avatar",
            "city",
            "country",
            "is_verified",
        ]
        read_only_fields = ["id", "user", "is_verified"]  # noqa: RUF012

    @extend_schema_field(serializers.CharField)
    def get_full_name(self, obj):
        """
        Returns user's full name or username.
        Retorna nome completo ou username do usuário.
        """
        return obj.user.get_full_name() or obj.user.username
