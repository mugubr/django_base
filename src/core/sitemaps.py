"""
Sitemaps for SEO optimization.
Sitemaps para otimização SEO.

This module defines Django sitemaps for search engine crawlers.
Este módulo define sitemaps Django para crawlers de mecanismos de busca.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Product


class StaticViewSitemap(Sitemap):
    """
    Sitemap for static pages (home, about, products listing, etc.).
    Sitemap para páginas estáticas (home, sobre, listagem de produtos, etc.).
    """

    priority = 0.8
    changefreq = "daily"

    def items(self):
        """
        Return list of URL names for static pages.
        Retorna lista de nomes de URLs para páginas estáticas.
        """
        return ["home", "about", "products", "login", "register"]

    def location(self, item):
        """
        Return the URL for each item.
        Retorna a URL para cada item.
        """
        return reverse(item)


class ProductSitemap(Sitemap):
    """
    Sitemap for product pages.
    Sitemap para páginas de produtos.
    """

    changefreq = "weekly"
    priority = 0.7

    def items(self):
        """
        Return all active products.
        Retorna todos os produtos ativos.
        """
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        """
        Return last modification date.
        Retorna data da última modificação.
        """
        return obj.updated_at
