"""
Integration Tests for API Workflows.
Testes de Integração para Fluxos de Trabalho da API.

Tests complete API workflows including authentication, CRUD operations,
and relationships between models.

Testa fluxos completos da API incluindo autenticação, operações CRUD
e relacionamentos entre modelos.
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.factories import CategoryFactory, ProductFactory, TagFactory, UserFactory
from core.models import Product

User = get_user_model()


class ProductAPIIntegrationTest(APITestCase):
    """
    Integration tests for Product API workflow.
    Testes de integração para fluxo de trabalho da API de Product.
    """

    def setUp(self):
        """Set up test data / Configurar dados de teste"""
        self.user = UserFactory()
        self.category = CategoryFactory()
        self.tags = [TagFactory() for _ in range(3)]

    def test_product_crud_workflow(self):
        """
        Test complete CRUD workflow for products.
        Testa fluxo CRUD completo para produtos.
        """
        # Authenticate / Autenticar
        self.client.force_authenticate(user=self.user)

        # CREATE: Create new product / Criar novo produto
        create_url = reverse("product-list")
        create_data = {
            "name": "Test Product",
            "price": "99.99",
            "stock": 10,
            "category": self.category.id,
            "tags": [tag.id for tag in self.tags],
        }
        response = self.client.post(create_url, create_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product_id = response.data["id"]

        # READ: Retrieve product / Recuperar produto
        detail_url = reverse("product-detail", kwargs={"pk": product_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Product")
        self.assertEqual(Decimal(response.data["price"]), Decimal("99.99"))

        # UPDATE: Update product / Atualizar produto
        update_data = {"name": "Updated Product", "price": "149.99"}
        response = self.client.patch(detail_url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Product")

        # DELETE: Soft delete product / Soft delete produto
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify soft delete / Verificar soft delete
        product = Product.objects.get(id=product_id)
        self.assertTrue(product.is_deleted)

    def test_product_filtering_workflow(self):
        """
        Test product filtering and search.
        Testa filtragem e busca de produtos.
        """
        # Create test products / Criar produtos de teste
        ProductFactory.create_batch(5, category=self.category, price=Decimal("50.00"))
        ProductFactory.create_batch(3, category=self.category, price=Decimal("150.00"))

        list_url = reverse("product-list")

        # Filter by price range / Filtrar por faixa de preço
        response = self.client.get(list_url, {"price__gte": 100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

        # Search by name / Buscar por nome
        ProductFactory(name="Unique Product Name")
        response = self.client.get(list_url, {"search": "Unique"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)


class AuthenticationIntegrationTest(APITestCase):
    """
    Integration tests for authentication workflow.
    Testes de integração para fluxo de autenticação.
    """

    def test_user_registration_to_profile_workflow(self):
        """
        Test user registration → profile creation → profile update workflow.
        Testa fluxo de registro → criação perfil → atualização perfil.
        """
        # User registration (handled by UserProfile signal)
        # Registro de usuário (gerenciado pelo signal UserProfile)
        user = UserFactory()

        # Verify profile was auto-created / Verificar perfil foi auto-criado
        self.assertTrue(hasattr(user, "profile"))

        # Authenticate / Autenticar
        self.client.force_authenticate(user=user)

        # Update profile / Atualizar perfil
        profile_url = reverse("userprofile-detail", kwargs={"pk": user.profile.id})
        update_data = {
            "bio": "Updated bio",
            "location": "São Paulo",
        }
        response = self.client.patch(profile_url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio"], "Updated bio")


class CategoryHierarchyIntegrationTest(APITestCase):
    """
    Integration tests for category hierarchy.
    Testes de integração para hierarquia de categorias.
    """

    def setUp(self):
        """Set up test data / Configurar dados de teste"""
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_category_tree_workflow(self):
        """
        Test category tree creation and retrieval.
        Testa criação e recuperação de árvore de categorias.
        """
        # Create parent category / Criar categoria pai
        parent = CategoryFactory(name="Electronics")

        # Create child categories / Criar categorias filhas
        CategoryFactory(name="Computers", parent=parent)
        CategoryFactory(name="Phones", parent=parent)

        # Get category tree / Obter árvore de categorias
        tree_url = reverse("category-tree")
        response = self.client.get(tree_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify tree structure / Verificar estrutura da árvore
        self.assertGreater(len(response.data), 0)
