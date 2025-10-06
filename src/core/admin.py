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
        "is_active",
        "created_at",
        "created_by",
    )
    list_filter = ("is_active", "category", "tags", "created_at")
    search_fields = ("name",)
    filter_horizontal = ("tags",)
    readonly_fields = ("created_at", "updated_at")

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
    list_display = ("name", "slug", "parent", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}  # noqa: RUF012
    readonly_fields = ("created_at", "updated_at")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}  # noqa: RUF012
    readonly_fields = ("created_at",)
