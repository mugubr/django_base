from django.contrib import admin
from django.shortcuts import render
from django.urls import path

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Customizes the Django admin interface for the Product model.
    Customiza a interface do admin do Django para o modelo Product.
    """

    # list_display: Configures the columns shown in the product list page.
    # list_display: Configura as colunas exibidas na página de listagem
    # de produtos.
    list_display = ("name", "price", "created_at")

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
