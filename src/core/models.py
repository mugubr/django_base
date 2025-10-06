# Product Model - Core Application
# Modelo de Produto - Aplicação Core

# This module defines the Product model with enhanced features including:
# - Database indexing for performance
# - Custom validation logic
# - Useful property methods
# - Soft delete capability
#
# Este módulo define o modelo Product com recursos aprimorados incluindo:
# - Indexação de banco de dados para performance
# - Lógica de validação customizada
# - Métodos de propriedade úteis
# - Capacidade de soft delete

from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Product(models.Model):
    """
    Represents a product in the system with complete
    validation and business logic.

    Fields:
        name: Product name (max 100 characters, indexed)
        price: Product price (decimal with 10 digits, 2 decimal places)
        created_at: Timestamp when product was created (auto-generated)
        updated_at: Timestamp when product was last updated (auto-updated)
        is_active: Soft delete flag (allows "deleting" without removing
        from DB)

    Representa um produto no sistema com validação completa e lógica de
    negócio.

    Campos:
        name: Nome do produto (máx 100 caracteres, indexado)
        price: Preço do produto (decimal com 10 dígitos, 2 casas decimais)
        created_at: Timestamp de quando o produto foi criado (auto-gerado)
        updated_at: Timestamp da última atualização do
        produto (auto-atualizado)
        is_active: Flag de soft delete (permite "deletar" sem remover do BD)
    """

    # Database Fields / Campos do Banco de Dados

    name = models.CharField(
        max_length=100,
        db_index=True,  # Index for faster queries by name / Índice para consultas mais rápidas pelo nome  # noqa: E501
        verbose_name="Product Name",
        help_text="The name of the product (max 100 characters) / "
        "O nome do produto (máximo 100 caracteres)",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Price",
        help_text="Product price in currency units / Preço do produto "
        "em unidades monetárias",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,  # Automatically set when object is first created / Automaticamente definido quando o objeto é criado pela primeira vez  # noqa: E501
        verbose_name="Created At",
        help_text="Timestamp when the product was created / "
        "Timestamp de quando o produto foi criado",
    )

    updated_at = models.DateTimeField(
        auto_now=True,  # Automatically updated on every save
        verbose_name="Updated At",
        help_text="Timestamp when the product was last updated / "
        "Timestamp da última atualização do produto",
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,  # Index for filtering active/inactive products
        verbose_name="Is Active",
        help_text="Indicates if the product is active (soft delete) / "
        "Indica se o produto está ativo (soft delete)",
    )

    # Meta Options / Opções Meta

    class Meta:
        # Default ordering when querying products (newest first)
        # Ordenação padrão ao consultar produtos (mais recentes primeiro)
        ordering = ["-created_at"]  # noqa: RUF012

        # Human-readable names for admin interface
        # Nomes legíveis para interface administrativa
        verbose_name = "Product"
        verbose_name_plural = "Products"

        # Database indexes for query optimization
        # Índices de banco de dados para otimização de queries
        indexes = [  # noqa: RUF012
            # Composite index for common query pattern: active products by
            # creation date
            # Índice composto para padrão comum de consulta: produtos
            # ativos por data de criação
            models.Index(
                fields=["is_active", "-created_at"], name="active_created_idx"
            ),
            # Index for searching products by name
            # Índice para busca de produtos por nome
            models.Index(fields=["name"], name="name_idx"),
            # Index for price-based queries
            # Índice para consultas baseadas em preço
            models.Index(fields=["price"], name="price_idx"),
        ]

        # Permissions for fine-grained access control
        # Permissões para controle de acesso granular
        permissions = [  # noqa: RUF012
            ("can_deactivate_product", "Can deactivate product"),
            ("can_set_special_price", "Can set special pricing"),
        ]

    # Custom Validation / Validação Customizada

    def clean(self):
        """
        Custom validation logic executed before saving.
        Raises ValidationError if data is invalid.

        Lógica de validação customizada executada antes de salvar.
        Lança ValidationError se os dados forem inválidos.
        """
        super().clean()

        # Validate price is positive
        # Valida se o preço é positivo
        if self.price is not None and self.price <= 0:
            raise ValidationError(
                {
                    "price": "Price must be greater than zero. / "
                    "O preço deve ser maior que zero."
                }
            )

        # Validate price doesn't exceed maximum
        # Valida se o preço não excede o máximo
        if self.price is not None and self.price > Decimal("9999999.99"):
            raise ValidationError(
                {
                    "price": "Price exceeds maximum allowed value. / "
                    "O preço excede o valor máximo permitido."
                }
            )

        # Validate name is not empty or whitespace
        # Valida se o nome não está vazio ou só com espaços
        if self.name and not self.name.strip():
            raise ValidationError(
                {
                    "name": "Product name cannot be empty "
                    "or whitespace only. / "
                    "O nome do produto não pode ser vazio "
                    "ou conter apenas espaços."
                }
            )

        # Validate name length
        # Valida comprimento do nome
        if self.name and len(self.name.strip()) < 3:
            raise ValidationError(
                {
                    "name": "Product name must have at least 3 characters. / "
                    "O nome do produto deve ter pelo menos 3 caracteres."
                }
            )

    def save(self, *args, **kwargs):  # noqa: DJ012
        """
        Override save to execute validation before saving.
        This ensures data integrity at the application level.

        Sobrescreve save para executar validação antes de salvar.
        Isso garante integridade de dados no nível da aplicação.
        """
        # Run validation
        # Executa validação
        self.full_clean()

        # Strip whitespace from name
        # Remove espaços em branco do nome
        if self.name:
            self.name = self.name.strip()

        # Call parent save method
        # Chama método save da classe pai
        super().save(*args, **kwargs)

    # String Representations / Representações em String

    def __str__(self):  # noqa: DJ012
        """
        Human-readable string representation used in Django admin and shell.
        Representação em string legível usada no admin Django e shell.
        """
        return self.name

    def __repr__(self):
        """
        Developer-friendly representation for debugging.
        Representação amigável para desenvolvedores para debugging.
        """
        return (
            f"<Product id={self.id} name='{self.name}' "
            f"price={self.price} active={self.is_active}>"
        )

    # Property Methods / Métodos de Propriedade

    @property
    def is_new(self):
        """
        Checks if the product was created within the last 7 days.
        Useful for displaying "NEW" badges in the frontend.

        Verifica se o produto foi criado nos últimos 7 dias.
        Útil para exibir badges "NOVO" no frontend.

        Returns:
            bool: True if product is less than 7 days old
        """
        if not self.created_at:
            return False
        return self.created_at >= timezone.now() - timedelta(days=7)

    @property
    def formatted_price(self):
        """
        Returns price formatted with currency symbol.
        Can be customized based on locale/currency settings.

        Retorna preço formatado com símbolo de moeda.
        Pode ser customizado baseado em configurações de locale/moeda.

        Returns:
            str: Formatted price string (e.g., "R$ 99.99")
        """
        return f"R$ {self.price:.2f}"

    @property
    def age_in_days(self):
        """
        Calculate how many days since the product was created.
        Useful for analytics and reporting.

        Calcula quantos dias desde que o produto foi criado.
        Útil para analytics e relatórios.

        Returns:
            int: Number of days since creation
        """
        if not self.created_at:
            return 0
        delta = timezone.now() - self.created_at
        return delta.days

    # Business Logic Methods / Métodos de Lógica de Negócio

    def apply_discount(self, percentage):
        """
        Applies a percentage discount to the product price.
        Validates discount percentage and updates price.

        Aplica um desconto percentual ao preço do produto.
        Valida percentual de desconto e atualiza preço.

        Args:
            percentage (float): Discount percentage (0-100)

        Raises:
            ValueError: If percentage is not between 0 and 100

        Example:
            product.apply_discount(10)  # Apply 10% discount
        """
        if not 0 < percentage < 100:
            raise ValueError(
                "Discount percentage must be between 0 and 100. / "
                "Percentual de desconto deve estar entre 0 e 100."
            )

        discount_amount = self.price * (Decimal(str(percentage)) / Decimal("100"))
        self.price -= discount_amount
        self.save()

    def deactivate(self):
        """
        Soft delete: Mark product as inactive instead of
        deleting from database.
        This preserves data integrity and allows for recovery.

        Soft delete: Marca produto como inativo ao invés de deletar do banco de dados.
        Isso preserva integridade de dados e permite recuperação.
        """
        self.is_active = False
        self.save(update_fields=["is_active", "updated_at"])

    def activate(self):
        """
        Reactivate a previously deactivated product.
        Reativa um produto previamente desativado.
        """
        self.is_active = True
        self.save(update_fields=["is_active", "updated_at"])

    def duplicate(self):
        """
        Creates a duplicate of this product with a modified name.
        Useful for creating product variations.

        Cria uma duplicata deste produto com nome modificado.
        Útil para criar variações de produtos.

        Returns:
            Product: New product instance (not saved to database)
        """
        return Product(
            name=f"{self.name} (Copy)",
            price=self.price,
            is_active=self.is_active,
        )

    # Query Helpers / Auxiliares de Consulta

    @classmethod
    def active_products(cls):
        """
        Returns queryset of only active products.
        Retorna queryset apenas de produtos ativos.

        Returns:
            QuerySet: Filtered queryset of active products
        """
        return cls.objects.filter(is_active=True)

    @classmethod
    def get_recent(cls, days=7):
        """
        Get products created within the specified number of days.
        Obtém produtos criados dentro do número especificado de dias.

        Args:
            days (int): Number of days to look back

        Returns:
            QuerySet: Recent products
        """
        cutoff_date = timezone.now() - timedelta(days=days)
        return cls.objects.filter(created_at__gte=cutoff_date, is_active=True)

    @classmethod
    def get_price_range(cls, min_price, max_price):
        """
        Get products within a specific price range.
        Obtém produtos dentro de uma faixa de preço específica.

        Args:
            min_price (Decimal): Minimum price
            max_price (Decimal): Maximum price

        Returns:
            QuerySet: Products in price range
        """
        return cls.objects.filter(
            price__gte=min_price, price__lte=max_price, is_active=True
        )
