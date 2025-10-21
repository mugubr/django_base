"""
Model Tests for Core Application.
Testes de Modelos para Aplicação Core.

Tests core model functionality including soft delete, validation, and business logic.
Testa funcionalidade principal dos modelos incluindo soft delete, validação e lógica de negócio.
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from core.factories import CategoryFactory, ProductFactory, TagFactory, UserFactory
from core.models import Category, Product, Tag

User = get_user_model()


class ProductModelTest(TestCase):
    """
    Tests for Product model.
    Testes para modelo Product.
    """

    def setUp(self):
        """Set up test data / Configurar dados de teste"""
        self.user = UserFactory()
        self.category = CategoryFactory()
        self.product = ProductFactory(created_by=self.user, category=self.category)

    def test_product_creation(self):
        """Test Product instance creation / Testa criação de instância Product"""
        self.assertIsInstance(self.product, Product)
        self.assertEqual(self.product.created_by, self.user)
        self.assertFalse(self.product.is_deleted)

    def test_product_str(self):
        """Test Product __str__ method / Testa método __str__ do Product"""
        self.assertEqual(str(self.product), self.product.name)

    def test_product_soft_delete(self):
        """Test Product soft_delete() method / Testa método soft_delete() do Product"""
        self.product.soft_delete()
        self.product.refresh_from_db()
        self.assertTrue(self.product.is_deleted)
        self.assertIsNotNone(self.product.deleted_at)

    def test_product_restore(self):
        """Test Product restore() method / Testa método restore() do Product"""
        self.product.soft_delete()
        self.product.restore()
        self.product.refresh_from_db()
        self.assertFalse(self.product.is_deleted)
        self.assertIsNone(self.product.deleted_at)

    def test_product_formatted_price(self):
        """Test Product.formatted_price property / Testa propriedade Product.formatted_price"""
        self.product.price = Decimal("99.99")
        self.product.save()
        self.assertEqual(self.product.formatted_price, "R$ 99.99")

    def test_product_apply_discount(self):
        """Test Product.apply_discount() method / Testa método Product.apply_discount()"""
        original_price = Decimal("100.00")
        self.product.price = original_price
        self.product.save()

        self.product.apply_discount(10)
        self.product.refresh_from_db()

        expected_price = Decimal("90.00")
        self.assertEqual(self.product.price, expected_price)


class CategoryModelTest(TestCase):
    """
    Tests for Category model.
    Testes para modelo Category.
    """

    def setUp(self):
        """Set up test data / Configurar dados de teste"""
        self.user = UserFactory()
        self.category = CategoryFactory(created_by=self.user)

    def test_category_creation(self):
        """Test Category instance creation / Testa criação de instância Category"""
        self.assertIsInstance(self.category, Category)
        self.assertFalse(self.category.is_deleted)

    def test_category_str(self):
        """Test Category __str__ method / Testa método __str__ do Category"""
        self.assertEqual(str(self.category), self.category.name)

    def test_category_hierarchy(self):
        """Test Category parent-child relationship / Testa relacionamento pai-filho de Category"""
        child = CategoryFactory(parent=self.category, created_by=self.user)
        self.assertEqual(child.parent, self.category)
        self.assertIn(child, self.category.children.all())

    def test_category_soft_delete(self):
        """Test Category soft_delete() method / Testa método soft_delete() do Category"""
        self.category.soft_delete()
        self.category.refresh_from_db()
        self.assertTrue(self.category.is_deleted)
        self.assertIsNotNone(self.category.deleted_at)


class TagModelTest(TestCase):
    """
    Tests for Tag model.
    Testes para modelo Tag.
    """

    def setUp(self):
        """Set up test data / Configurar dados de teste"""
        self.user = UserFactory()
        self.tag = TagFactory(created_by=self.user)

    def test_tag_creation(self):
        """Test Tag instance creation / Testa criação de instância Tag"""
        self.assertIsInstance(self.tag, Tag)
        self.assertEqual(self.tag.created_by, self.user)

    def test_tag_str(self):
        """Test Tag __str__ method / Testa método __str__ do Tag"""
        self.assertEqual(str(self.tag), self.tag.name)
