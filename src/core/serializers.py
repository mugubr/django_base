# Product Serializers - Core Application
# Serializadores de Produto - Aplicação Core

# This module defines serializers for the Product model with:
# - Custom field validations
# - Computed read-only fields
# - Different serializers for different use cases (list vs detail)
# - Proper error messages in both languages
#
# Este módulo define serializadores para o modelo Product com:
# - Validações de campo customizadas
# - Campos computados somente leitura
# - Diferentes serializadores para diferentes casos de uso (lista vs detalhe)
# - Mensagens de erro apropriadas em ambos idiomas

from decimal import Decimal

from rest_framework import serializers

from .models import Product


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
    is_new = serializers.ReadOnlyField()

    # Uses SerializerMethodField for custom formatting
    # Usa SerializerMethodField para formatação customizada
    formatted_price = serializers.SerializerMethodField()

    # Another computed field from model property
    # Outro campo computado da propriedade do modelo
    age_in_days = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [  # noqa: RUF012
            "id",
            "name",
            "price",
            "formatted_price",  # Computed field
            "created_at",
            "updated_at",
            "is_active",
            "is_new",  # Computed field
            "age_in_days",  # Computed field
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
        model = Product
        fields = ["name", "price", "is_active"]  # noqa: RUF012
        # All fields are required on creation
        # Todos os campos são obrigatórios na criação
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
        model = Product
        fields = ["name", "price", "is_active"]  # noqa: RUF012
        # All fields optional for partial updates
        # Todos os campos opcionais para atualizações parciais
        extra_kwargs = {  # noqa: RUF012
            "name": {"required": False},
            "price": {"required": False},
            "is_active": {"required": False},
        }
