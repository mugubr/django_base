"""
Django Admin Customizations - Core Application
Customizações do Django Admin - Aplicação Core

This module configures the Django admin interface for core models with:
- Custom list displays, filters, and search fields
- Custom admin views (e.g., datatable view)
- Readonly fields and fieldsets for better organization
- Horizontal filters for many-to-many relationships

Este módulo configura a interface do Django admin para modelos core com:
- Displays de lista, filtros e campos de busca customizados
- Views admin customizadas (ex: view de datatable)
- Campos readonly e fieldsets para melhor organização
- Filtros horizontais para relacionamentos many-to-many
"""

from django.contrib import admin
from django.shortcuts import render
from django.urls import path

from .models import Category, Product, Tag, UserProfile


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Customizes the Django admin interface for the Product model.
    Customiza a interface do admin do Django para o modelo Product.
    """

    list_display = (
        "name",
        "price",
        "category",
        "stock",
        "is_deleted",
        "created_by",
        "updated_by",
        "created_at",
    )
    list_filter = ("is_deleted", "category", "tags", "created_at")
    search_fields = ("name",)
    filter_horizontal = ("tags",)
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
        "created_by",
        "updated_by",
    )

    def get_urls(self):
        """
        Adds custom URLs to the admin for this model.
        Adiciona URLs personalizadas ao admin para este modelo.
        """
        urls = super().get_urls()
        custom_urls = [
            # Path for our custom datatable view.
            # Caminho para nossa view de datatable personalizada.
            path(
                "datatable/",
                self.admin_site.admin_view(self.datatable_view),
                name="product-datatable",
            ),
        ]
        return custom_urls + urls

    def datatable_view(self, request):
        """
        A custom admin view that renders a template with an interactive table.
        Uma view de admin personalizada que renderiza um template com uma
        tabela interativa.
        """
        products = Product.objects.all()
        context = {
            **self.admin_site.each_context(request),
            "products": products,
            "title": "Relatório de Produtos Interativo",
        }
        return render(request, "admin/product_datatable.html", context)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserProfile model with organized fieldsets.
    Configuração admin para modelo UserProfile com fieldsets organizados.

    Fields/Campos:
        - list_display: Columns shown in list view / Colunas mostradas na listagem
        - list_filter: Filterable fields / Campos filtráveis
        - search_fields: Searchable fields (includes related user fields) / Campos pesquisáveis (inclui campos de usuário relacionado)
        - readonly_fields: Auto-populated timestamp fields / Campos de timestamp auto-populados
        - fieldsets: Grouped field sections / Seções de campos agrupadas
    """

    list_display = ("user", "city", "country", "is_verified", "created_at")
    list_filter = ("is_verified", "country", "created_at")
    search_fields = ("user__username", "user__email", "bio", "city")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("User Info", {"fields": ("user", "bio", "avatar")}),
        ("Contact", {"fields": ("phone", "website")}),
        ("Location", {"fields": ("city", "country")}),
        ("Status", {"fields": ("is_verified", "birth_date")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model with slug auto-population.
    Configuração admin para modelo Category com auto-população de slug.

    Fields/Campos:
        - prepopulated_fields: Auto-generates slug from name / Auto-gera slug a partir do nome
        - list_display: Shows hierarchical categories / Mostra categorias hierárquicas
        - search_fields: Searches in name and description / Busca em nome e descrição
    """

    list_display = ("name", "slug", "parent", "is_deleted", "created_by", "created_at")
    list_filter = ("is_deleted", "created_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
        "created_by",
        "updated_by",
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin configuration for Tag model with color display.
    Configuração admin para modelo Tag com exibição de cor.

    Fields/Campos:
        - list_display: Shows tag name, slug, and color / Mostra nome, slug e cor da tag
        - prepopulated_fields: Auto-generates slug / Auto-gera slug
    """

    list_display = ("name", "slug", "color", "created_by", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
