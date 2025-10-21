# Core Models - Django Base Project
# Modelos Core - Projeto Django Base

# This module defines all data models for the core application with:
# - Product model with validation and business logic
# - UserProfile with extended user information
# - Category and Tag models with many-to-many relationships
# - Timestamp tracking and soft delete functionality
#
# Este módulo define todos os modelos de dados para a aplicação core com:
# - Modelo Product com validação e lógica de negócio
# - UserProfile com informações estendidas do usuário
# - Modelos Category e Tag com relacionamentos muitos-para-muitos
# - Rastreamento de timestamps e funcionalidade de soft delete

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from core.mixins import (
    SoftDeleteModelMixin,
    TimeStampedModelMixin,
    UserTrackingModelMixin,
)

if TYPE_CHECKING:
    pass

User = get_user_model()


class Product(TimeStampedModelMixin, SoftDeleteModelMixin, UserTrackingModelMixin):
    """
    Represents a product in the system with complete validation and business logic.
    Uses mixins for timestamp, soft delete, and user tracking functionality.

    Mixins:
        TimeStampedModelMixin: Provides created_at and updated_at fields
        SoftDeleteModelMixin: Provides is_deleted, deleted_at, soft_delete(), restore()
        UserTrackingModelMixin: Provides created_by and updated_by fields

    Fields:
        name: Product name (max 200 characters, indexed, required)
        price: Product price (decimal with 10 digits, 2 decimal places, required)
        stock: Product stock quantity (integer, default 0)
        category: ForeignKey to Category (optional)
        tags: ManyToMany to Tag (optional)

    Representa um produto no sistema com validação completa e lógica de negócio.
    Usa mixins para timestamp, soft delete e rastreamento de usuário.

    Mixins:
        TimeStampedModelMixin: Fornece campos created_at e updated_at
        SoftDeleteModelMixin: Fornece is_deleted, deleted_at, soft_delete(), restore()
        UserTrackingModelMixin: Fornece campos created_by e updated_by

    Campos:
        name: Nome do produto (máx 200 caracteres, indexado, obrigatório)
        price: Preço do produto (decimal com 10 dígitos, 2 casas decimais, obrigatório)
        stock: Quantidade em estoque (inteiro, padrão 0)
        category: ForeignKey para Category (opcional)
        tags: ManyToMany para Tag (opcional)
    """

    # Database Fields / Campos do Banco de Dados

    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name=_("Product Name"),
        help_text=_(
            "The name of the product (max 200 characters) / Nome do produto (máx 200 caracteres)"
        ),
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Price"),
        help_text=_(
            "Product price in currency units / Preço do produto em unidades monetárias"
        ),
    )

    stock = models.IntegerField(
        default=0,
        verbose_name=_("Stock"),
        help_text=_("Product stock quantity / Quantidade em estoque do produto"),
    )

    # Relationships / Relacionamentos

    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name=_("Category"),
        help_text=_("Product category"),
    )

    tags = models.ManyToManyField(
        "Tag",
        blank=True,
        related_name="products",
        verbose_name=_("Tags"),
        help_text=_("Product tags / Tags do produto"),
    )

    # Meta Options / Opções Meta

    class Meta:
        # Default ordering when querying products (newest first)
        # Ordenação padrão ao consultar produtos (mais recentes primeiro)
        ordering = ["-created_at"]

        # Human-readable names for admin interface
        # Nomes legíveis para interface administrativa
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

        # Database indexes for query optimization
        # Índices de banco de dados para otimização de queries
        indexes = [
            # Composite index for common query pattern: non-deleted products by
            # creation date
            # Índice composto para padrão comum de consulta: produtos
            # não deletados por data de criação
            models.Index(
                fields=["is_deleted", "-created_at"], name="deleted_created_idx"
            ),
            # Index for searching products by name
            # Índice para busca de produtos por nome
            models.Index(fields=["name"], name="name_idx"),
            # Index for price-based queries
            # Índice para consultas baseadas em preço
            models.Index(fields=["price"], name="price_idx"),
            # Index for stock queries
            # Índice para consultas de estoque
            models.Index(fields=["stock"], name="stock_idx"),
        ]

        # Permissions for fine-grained access control
        # Permissões para controle de acesso granular
        permissions = [
            ("can_delete_product", "Can soft delete product"),
            ("can_set_special_price", "Can set special pricing"),
        ]

    # Custom Validation / Validação Customizada

    def clean(self) -> None:
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

        # Validate stock is non-negative / Valida se estoque não é negativo
        if self.stock is not None and self.stock < 0:
            raise ValidationError(
                {"stock": "Stock cannot be negative. / Estoque não pode ser negativo."}
            )

        # Validate stock maximum / Valida máximo de estoque
        if self.stock is not None and self.stock > 1000000:
            raise ValidationError(
                {
                    "stock": "Stock cannot exceed 1,000,000 units. / "
                    "Estoque não pode exceder 1.000.000 unidades."
                }
            )

    def save(self, *args: Any, **kwargs: Any) -> None:
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

    def __str__(self) -> str:
        """
        Human-readable string representation used in Django admin and shell.
        Representação em string legível usada no admin Django e shell.
        """
        return self.name

    def __repr__(self) -> str:
        """
        Developer-friendly representation for debugging.
        Representação amigável para desenvolvedores para debugging.
        """
        return (
            f"<Product id={self.id} name='{self.name}' "  # type: ignore
            f"price={self.price} deleted={self.is_deleted}>"
        )

    # Property Methods / Métodos de Propriedade

    @property
    def is_new(self) -> bool:
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
    def formatted_price(self) -> str:
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
    def age_in_days(self) -> int:
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

    def apply_discount(self, percentage: float) -> None:
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
        self.price = (self.price - discount_amount).quantize(Decimal("0.01"))
        self.save()

    # Note: deactivate() and activate() removed - use soft_delete() and restore() from SoftDeleteModelMixin
    # Nota: deactivate() e activate() removidos - use soft_delete() e restore() do SoftDeleteModelMixin

    def duplicate(self) -> Product:
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
            is_deleted=self.is_deleted,
        )

    # Query Helpers / Auxiliares de Consulta

    @classmethod
    def active_products(cls) -> QuerySet[Product]:
        """
        Returns queryset of only active products.
        Retorna queryset apenas de produtos ativos.

        Returns:
            QuerySet: Filtered queryset of active products
        """
        return cls.objects.filter(is_deleted=False)

    @classmethod
    def get_recent(cls, days: int = 7) -> QuerySet[Product]:
        """
        Get products created within the specified number of days.
        Obtém produtos criados dentro do número especificado de dias.

        Args:
            days (int): Number of days to look back

        Returns:
            QuerySet: Recent products
        """
        cutoff_date = timezone.now() - timedelta(days=days)
        return cls.objects.filter(created_at__gte=cutoff_date, is_deleted=False)

    @classmethod
    def get_price_range(
        cls, min_price: Decimal, max_price: Decimal
    ) -> QuerySet[Product]:
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
            price__gte=min_price, price__lte=max_price, is_deleted=False
        )


# User Profile Model / Modelo de Perfil de Usuário


class UserProfile(TimeStampedModelMixin):
    """
    Extended user profile with additional information beyond default Django User.
    One-to-one relationship with Django User model - automatically created via signals.

    Uses TimeStampedModelMixin for automatic timestamp management.

    Fields:
        user: OneToOne link to Django User (CASCADE delete)
        bio: Text biography (max 500 chars, optional)
        avatar: Profile image uploaded to avatars/%Y/%m/%d/ (optional)
        phone: Phone number with international format support (optional)
        birth_date: User's birth date (optional)
        city: City name (max 100 chars, optional)
        country: Country name (max 100 chars, optional)
        website: Personal website URL (optional)
        is_verified: Verification status flag (default False)

    Mixins:
        TimeStampedModelMixin: Provides created_at and updated_at fields

    Perfil de usuário estendido com informações adicionais além do User padrão do Django.
    Relacionamento um-para-um com modelo User do Django - criado automaticamente via signals.

    Usa TimeStampedModelMixin para gerenciamento automático de timestamps.

    Campos:
        user: Link OneToOne para Django User (delete CASCADE)
        bio: Biografia de texto (máx 500 chars, opcional)
        avatar: Imagem de perfil enviada para avatars/%Y/%m/%d/ (opcional)
        phone: Número de telefone com suporte a formato internacional (opcional)
        birth_date: Data de nascimento do usuário (opcional)
        city: Nome da cidade (máx 100 chars, opcional)
        country: Nome do país (máx 100 chars, opcional)
        website: URL do website pessoal (opcional)
        is_verified: Flag de status de verificação (padrão False)

    Mixins:
        TimeStampedModelMixin: Fornece campos created_at e updated_at

    Examples / Exemplos:
        # Access user's profile / Acessar perfil do usuário
        profile = user.profile

        # Update profile / Atualizar perfil
        profile.bio = "Software developer"
        profile.city = "São Paulo"
        profile.save()

        # Check if user is verified / Verificar se usuário é verificado
        if user.profile.is_verified:
            # Grant access / Conceder acesso
            pass
    """

    # User relationship / Relacionamento com usuário
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,  # Delete profile when user is deleted / Deletar perfil quando usuário for deletado
        related_name="profile",
        verbose_name=_("User"),
        help_text=_("Related Django user / Usuário Django relacionado"),
    )

    # Personal information / Informações pessoais
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name=_("Biography"),
        help_text=_(
            "User biography (max 500 chars) / Biografia do usuário (máx 500 chars)"
        ),
    )

    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/%d/",  # Organized by date / Organizado por data
        blank=True,
        null=True,
        verbose_name=_("Avatar"),
        help_text=_("Profile picture / Foto de perfil"),
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Phone"),
        help_text=_(
            "Phone number with country code / Número de telefone com código do país"
        ),
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Birth date"),
        help_text=_("User's birth date / Data de nascimento do usuário"),
    )

    # Location information / Informações de localização
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("City"),
        help_text=_("User's city / Cidade do usuário"),
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Country"),
        help_text=_("User's country / País do usuário"),
    )

    # Online presence / Presença online
    website = models.URLField(
        blank=True,
        verbose_name=_("Website"),
        help_text=_("Personal website or portfolio / Website pessoal ou portfólio"),
    )

    # Verification status / Status de verificação
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_("Verified"),
        help_text=_("Indicates if user is verified / Indica se usuário é verificado"),
    )

    # Note: created_at, updated_at from TimeStampedModelMixin

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
        # Order by most recently created / Ordenar por mais recentemente criado
        ordering = ["-created_at"]
        # Add indexes for frequently queried fields / Adiciona indexes para campos frequentemente filtrados na API
        indexes = [
            models.Index(fields=["is_verified"]),
            models.Index(fields=["city"]),
            models.Index(fields=["country"]),
        ]

    def __str__(self) -> str:
        """String representation showing username and verification status."""
        """Representação em string mostrando username e status de verificação."""
        verified = "✓" if self.is_verified else "✗"
        return f"{self.user.username}'s profile ({verified})"

    def __repr__(self) -> str:
        """Developer-friendly representation for debugging."""
        """Representação amigável para desenvolvedores para debugging."""
        return (
            f"<UserProfile user='{self.user.username}' "
            f"verified={self.is_verified} id={self.id}>"  # type: ignore
        )

    @property
    def full_name(self) -> str:
        """
        Get user's full name from related User model.
        Obtém nome completo do usuário do modelo User relacionado.

        Returns / Retorna:
            str: Full name or username if name not set
        """
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username

    @property
    def age(self) -> int | None:
        """
        Calculate user's age from birth_date.
        Calcula idade do usuário a partir da birth_date.

        Returns / Retorna:
            int | None: Age in years or None if birth_date not set
        """
        if not self.birth_date:
            return None
        today = timezone.now().date()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

    def verify(self) -> None:
        """
        Mark user profile as verified.
        Marca perfil de usuário como verificado.
        """
        self.is_verified = True
        self.save(update_fields=["is_verified", "updated_at"])

    def unverify(self) -> None:
        """
        Remove verification status from user profile.
        Remove status de verificação do perfil de usuário.
        """
        self.is_verified = False
        self.save(update_fields=["is_verified", "updated_at"])


# Category Model / Modelo de Categoria


class Category(TimeStampedModelMixin, SoftDeleteModelMixin, UserTrackingModelMixin):
    """
    Product category for organization and filtering with hierarchical structure.
    Self-referencing foreign key allows parent-child relationships (tree structure).

    Uses mixins for timestamps, soft delete, and user tracking.

    Fields:
        name: Category name (max 100 chars, unique, required)
        slug: URL-friendly slug (auto-generated from name, unique)
        description: Optional description text
        parent: Self-referencing FK for parent category (CASCADE delete, optional)

    Mixins:
        TimeStampedModelMixin: Provides created_at and updated_at fields
        SoftDeleteModelMixin: Provides is_deleted, deleted_at, soft_delete(), restore()
        UserTrackingModelMixin: Provides created_by and updated_by fields

    Categoria de produto para organização e filtragem com estrutura hierárquica.
    Chave estrangeira auto-referenciada permite relacionamentos pai-filho (estrutura de árvore).

    Usa mixins para timestamps, soft delete e rastreamento de usuário.

    Campos:
        name: Nome da categoria (máx 100 chars, único, obrigatório)
        slug: Slug amigável para URL (auto-gerado do nome, único)
        description: Texto de descrição opcional
        parent: FK auto-referenciada para categoria pai (delete CASCADE, opcional)

    Mixins:
        TimeStampedModelMixin: Fornece campos created_at e updated_at
        SoftDeleteModelMixin: Fornece is_deleted, deleted_at, soft_delete(), restore()
        UserTrackingModelMixin: Fornece campos created_by e updated_by

    Examples / Exemplos:
        # Create root category / Criar categoria raiz
        electronics = Category.objects.create(name="Electronics")

        # Create subcategory / Criar subcategoria
        laptops = Category.objects.create(
            name="Laptops",
            parent=electronics,
            description="Laptop computers"
        )

        # Get all children / Obter todos os filhos
        children = electronics.children.all()

        # Get parent / Obter pai
        parent = laptops.parent
    """

    # Basic fields / Campos básicos
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Name"),
        help_text=_("Category name (unique) / Nome da categoria (único)"),
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name=_("Slug"),
        help_text=_(
            "URL-friendly identifier (auto-generated) / Identificador amigável para URL (auto-gerado)"
        ),
    )

    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Category description / Descrição da categoria"),
    )

    # Hierarchical relationship / Relacionamento hierárquico
    parent = models.ForeignKey(
        "self",  # Self-referencing FK / FK auto-referenciada
        on_delete=models.CASCADE,  # Delete children when parent deleted / Deletar filhos quando pai deletado
        blank=True,
        null=True,
        related_name="children",  # Access children via parent.children.all()
        verbose_name=_("Parent category"),
        help_text=_(
            "Parent category for hierarchical structure / Categoria pai para estrutura hierárquica"
        ),
    )

    # Note: is_deleted, deleted_at from SoftDeleteModelMixin
    # Note: created_at, updated_at from TimeStampedModelMixin
    # Note: created_by, updated_by from UserTrackingModelMixin

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        # Order alphabetically / Ordenar alfabeticamente
        ordering = ["name"]
        # Add indexes for frequently filtered fields / Adiciona indexes para campos frequentemente filtrados
        indexes = [
            models.Index(fields=["is_deleted"]),
            models.Index(fields=["parent"]),
        ]

    def __str__(self) -> str:
        """String representation showing category hierarchy."""
        """Representação em string mostrando hierarquia de categoria."""
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    def __repr__(self) -> str:
        """Developer-friendly representation for debugging."""
        """Representação amigável para desenvolvedores para debugging."""
        return f"<Category id={self.id} name='{self.name}' parent={self.parent_id}>"  # type: ignore

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Auto-generate slug from name if not provided.
        Gera automaticamente slug a partir do nome se não fornecido.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def product_count(self) -> int:
        """
        Get count of active (not deleted) products in this category.
        Obtém contagem de produtos ativos (não deletados) nesta categoria.

        Returns / Retorna:
            int: Number of products
        """
        return self.products.filter(is_deleted=False).count()

    @property
    def is_root(self) -> bool:
        """
        Check if this is a root category (no parent).
        Verifica se esta é uma categoria raiz (sem pai).

        Returns / Retorna:
            bool: True if root category
        """
        return self.parent is None

    def get_ancestors(self) -> list[Category]:
        """
        Get all ancestor categories up to root.
        Obtém todas as categorias ancestrais até a raiz.

        Returns / Retorna:
            list[Category]: List of ancestor categories
        """
        ancestors: list[Category] = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors

    def get_descendants(self) -> list[Category]:
        """
        Get all descendant categories recursively.
        Obtém todas as categorias descendentes recursivamente.

        Returns / Retorna:
            list[Category]: List of descendant categories
        """
        descendants: list[Category] = []
        for child in self.children.all():
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants


# Tag Model / Modelo de Tag


class Tag(TimeStampedModelMixin, UserTrackingModelMixin):
    """
    Tag for flexible product labeling, filtering and search.
    Many-to-many relationship with products for flexible categorization.

    Uses mixins for timestamps and user tracking.

    Fields:
        name: Tag name (max 50 chars, unique, required)
        slug: URL-friendly slug (auto-generated from name, unique)
        color: Hex color code for UI display (default #6c757d - Bootstrap secondary)

    Mixins:
        TimeStampedModelMixin: Provides created_at and updated_at fields
        UserTrackingModelMixin: Provides created_by and updated_by fields

    Tag para rotulagem flexível, filtragem e busca de produtos.
    Relacionamento muitos-para-muitos com produtos para categorização flexível.

    Usa mixins para timestamps e rastreamento de usuário.

    Campos:
        name: Nome da tag (máx 50 chars, único, obrigatório)
        slug: Slug amigável para URL (auto-gerado do nome, único)
        color: Código de cor hex para exibição na UI (padrão #6c757d - Bootstrap secondary)

    Mixins:
        TimeStampedModelMixin: Fornece campos created_at e updated_at
        UserTrackingModelMixin: Fornece campos created_by e updated_by

    Examples / Exemplos:
        # Create tag / Criar tag
        tag = Tag.objects.create(
            name="Featured",
            color="#ff5722"  # Custom color / Cor customizada
        )

        # Add to product / Adicionar a produto
        product.tags.add(tag)

        # Get all products with tag / Obter todos os produtos com tag
        products = tag.products.all()

        # Get tag usage count / Obter contagem de uso da tag
        count = tag.product_count
    """

    # Basic fields / Campos básicos
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Name"),
        help_text=_("Tag name (unique) / Nome da tag (único)"),
    )

    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name=_("Slug"),
        help_text=_(
            "URL-friendly identifier (auto-generated) / Identificador amigável para URL (auto-gerado)"
        ),
    )

    color = models.CharField(
        max_length=7,  # Hex color format: #RRGGBB
        default="#6c757d",  # Bootstrap secondary color / Cor secundária do Bootstrap
        verbose_name=_("Color"),
        help_text=_(
            "Hex color code for badge display / Código de cor hex para exibição do badge"
        ),
    )

    # Note: created_at, updated_at from TimeStampedModelMixin
    # Note: created_by, updated_by from UserTrackingModelMixin

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        # Order alphabetically / Ordenar alfabeticamente
        ordering = ["name"]
        # Add index for color field / Adiciona index para o campo 'color'
        indexes = [
            models.Index(fields=["color"]),
        ]

    def __str__(self) -> str:
        """String representation showing tag name."""
        """Representação em string mostrando nome da tag."""
        return self.name

    def __repr__(self) -> str:
        """Developer-friendly representation for debugging."""
        """Representação amigável para desenvolvedores para debugging."""
        return f"<Tag id={self.id} name='{self.name}' color='{self.color}'>"  # type: ignore

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Auto-generate slug from name if not provided.
        Gera automaticamente slug a partir do nome se não fornecido.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def product_count(self) -> int:
        """
        Get count of products using this tag.
        Obtém contagem de produtos usando esta tag.

        Returns / Retorna:
            int: Number of products with this tag
        """
        return self.products.filter(is_deleted=False).count()

    @classmethod
    def get_popular(cls, limit: int = 10) -> QuerySet[Tag]:
        """
        Get most popular tags by product count.
        Obtém tags mais populares por contagem de produtos.

        Args / Argumentos:
            limit (int): Maximum number of tags to return / Número máximo de tags para retornar

        Returns / Retorna:
            QuerySet: Popular tags ordered by usage
        """
        from django.db.models import Count

        return (
            cls.objects.annotate(num_products=Count("products"))
            .filter(num_products__gt=0)
            .order_by("-num_products")[:limit]
        )
