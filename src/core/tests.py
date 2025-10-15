"""
Test Suite - Core Application
Suite de Testes - Aplicação Core

Comprehensive tests for:
- API endpoints (CRUD operations)
- Model methods and behaviors
- Signal integration with async tasks
- Authentication and permissions

Testes abrangentes para:
- Endpoints da API (operações CRUD)
- Métodos e comportamentos de modelos
- Integração de sinais com tarefas assíncronas
- Autenticação e permissões
"""

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import TestCase, override_settings
from django.urls import path
from rest_framework import status
from rest_framework.test import APIClient

from .decorators import rate_limit
from .models import Product

User = get_user_model()


class HelloAPITestCase(TestCase):
    """
    Tests for the hello_api view.
    Testes para a view hello_api.
    """

    def setUp(self):
        """
        Set up test fixtures before each test method.
        Configura fixtures de teste antes de cada método de teste.
        """
        # setUp runs before each test method. We create a client
        # to make API requests.
        # setUp executa antes de cada método de teste. Criamos um cliente
        # para fazer requisições à API.
        self.client = APIClient()


class ProductModelTestCase(TestCase):
    """
    Tests for the Product model.
    Testes para o modelo Product.
    """

    def test_product_str_representation(self):
        """
        Test that Product.__str__() returns the product name.
        Testa que Product.__str__() retorna o nome do produto.
        """
        # Creates a Product instance.
        # Cria uma instância de Product.
        product = Product.objects.create(name="Test Product", price="99.99")

        # Asserts that the __str__ method returns the product's name.
        # This will cover the missing line in `models.py`.
        # Garante que o método __str__ retorna o nome do produto.
        # Isso irá cobrir a linha faltante no `models.py`.
        self.assertEqual(str(product), "Test Product")


class ProductAPITestCase(TestCase):
    """
    Tests for the ProductViewSet (CRUD API endpoints).
    Testes para o ProductViewSet (endpoints da API de CRUD).
    """

    def setUp(self):
        """
        Set up test data: authenticated user and sample products.
        Configura dados de teste: usuário autenticado e produtos de exemplo.
        """
        self.client = APIClient()
        # Create a test user for authentication
        # Cria um usuário de teste para autenticação
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",  # noqa: S106
        )
        # Creates some initial products for testing GET requests.
        # Cria alguns produtos iniciais para testar requisições GET.
        Product.objects.create(name="Product A", price="10.00")
        Product.objects.create(name="Product B", price="20.00")

    def test_list_products(self):
        """
        Test GET /api/v1/products/ returns paginated product list.
        Testa que GET /api/v1/products/ retorna lista paginada de produtos.
        """
        # Tests the GET /api/v1/products/ endpoint.
        # Testa o endpoint GET /api/v1/products/.
        response = self.client.get("/api/v1/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Response is paginated, so we need to access 'results'
        # Resposta é paginada, então precisamos acessar 'results'
        self.assertIn("results", response.data)
        products = response.data["results"]
        # Asserts that the response contains at least 2 products.
        # Garante que a resposta contém pelo menos 2 produtos.
        self.assertGreaterEqual(len(products), 2)
        # Check that our test products exist in the response
        # Verifica que nossos produtos de teste existem na resposta
        product_names = [product["name"] for product in products]
        self.assertIn("Product A", product_names)
        self.assertIn("Product B", product_names)

    def test_create_product(self):
        """
        Test POST /api/v1/products/ creates a new product (requires auth).
        Testa que POST /api/v1/products/ cria um novo produto (requer autenticação).
        """
        # Tests the POST /api/v1/products/ endpoint.
        # Testa o endpoint POST /api/v1/products/.
        # Authenticate the client
        # Autentica o cliente
        self.client.force_authenticate(user=self.user)
        data = {"name": "Product C", "price": "30.00"}
        response = self.client.post("/api/v1/products/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Asserts that the product was actually created in the database.
        # Garante que o produto foi realmente criado no banco de dados.
        self.assertTrue(Product.objects.filter(name="Product C").exists())

    def test_retrieve_product(self):
        """
        Test GET /api/v1/products/{id}/ retrieves specific product.
        Testa que GET /api/v1/products/{id}/ recupera produto específico.
        """
        # Tests the GET /api/v1/products/{id}/ endpoint.
        # Testa o endpoint GET /api/v1/products/{id}/.
        product = Product.objects.get(name="Product A")
        response = self.client.get(f"/api/v1/products/{product.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Product A")


class ProductSignalTaskTestCase(TestCase):
    """
    Tests the integration between the post_save signal and the async task.
    Testa a integração entre o sinal post_save e a tarefa assíncrona.
    """

    # @patch intercepts the call to 'core.signals.async_task' and replaces
    # it with a mock.
    # The real task will not run, we just check if it was called correctly.
    # @patch intercepta a chamada para 'core.signals.async_task' e a substitui
    # por um mock.
    # A tarefa real não será executada, nós apenas verificamos se ela foi
    # chamada corretamente.
    @patch("core.signals.async_task")
    def test_creating_product_triggers_async_task(self, mock_async_task):
        """
        Test that creating a product triggers the notification async task.
        Testa que criar um produto dispara a tarefa assíncrona de notificação.

        Args/Argumentos:
            mock_async_task: Mocked async_task function / Função async_task mockada
        """
        # 'mock_async_task' is the mock object injected by @patch.
        # 'mock_async_task' é o objeto mock injetado pelo @patch.

        # Creating a product should trigger the post_save signal.
        # A criação de um produto deve disparar o sinal post_save.
        product = Product.objects.create(name="New Awesome Product", price="123.45")

        # Asserts that our mock task function was called exactly once.
        # This confirms the signal is working.
        # Garante que nossa função de tarefa mock foi chamada exatamente uma vez.
        # Isso confirma que o sinal está funcionando.
        mock_async_task.assert_called_once()

        # Asserts that the task was called with the correct arguments.
        # This is a very robust test.
        # Garante que a tarefa foi chamada com os argumentos corretos.
        # Este é um teste muito robusto.
        mock_async_task.assert_called_once_with(
            "core.tasks.notify_new_product",
            product_id=product.id,
            product_name=product.name,
        )

    @patch("core.signals.async_task")
    def test_updating_product_does_not_trigger_task(self, mock_async_task):
        """
        Test that updating a product does NOT trigger the notification task.
        Testa que atualizar um produto NÃO dispara a tarefa de notificação.

        Args/Argumentos:
            mock_async_task: Mocked async_task function / Função async_task mockada
        """
        # Creates a product initially. The task will be called here.
        # Cria um produto inicialmente. A tarefa será chamada aqui.
        product = Product.objects.create(name="Initial Product", price="10.00")

        # Resets the mock to clear the first call.
        # Reseta o mock para limpar a primeira chamada.
        mock_async_task.reset_mock()

        # Now, update the product. The signal will fire, but `created` will be False.
        # Agora, atualizamos o produto. O sinal vai disparar, mas `created` será False.
        product.price = "12.00"
        product.save()

        # Asserts that the async task was not called a second time.
        # Garante que a tarefa assíncrona não foi chamada uma segunda vez.
        mock_async_task.assert_not_called()


class AuthenticationTestCase(TestCase):
    """
    Tests for authentication views (login, register, logout).
    Testes para views de autenticação (login, registro, logout).
    """

    def setUp(self):
        """Set up test fixtures / Configura fixtures de teste"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="authuser",
            email="auth@example.com",
            password="testpass123",  # noqa: S106
        )

    def test_login_view_post_success(self):
        """Test POST /login/ with valid credentials / Testa POST /login/ com credenciais válidas"""
        response = self.client.post(
            "/login/",
            {"username": "authuser", "password": "testpass123"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_view(self):
        """Test GET /logout/ logs out user / Testa GET /logout/ desloga usuário"""
        self.client.force_login(self.user)
        response = self.client.get("/logout/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ViewTestCase(TestCase):
    """
    Tests for additional views (home, profile, products).
    Testes para views adicionais (home, perfil, produtos).
    """

    def setUp(self):
        """Set up test fixtures / Configura fixtures de teste"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="viewuser",
            email="view@example.com",
            password="testpass123",  # noqa: S106
        )

    def test_home_view(self):
        """Test GET / renders homepage / Testa GET / renderiza homepage"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_view_authenticated(self):
        """Test GET /profile/ for authenticated user / Testa GET /profile/ para usuário autenticado"""
        self.client.force_login(self.user)
        response = self.client.get("/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health_check_page(self):
        """Test GET /health-status/ renders health page / Testa GET /health-status/ renderiza página de saúde"""
        response = self.client.get("/health-status/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ModelMethodsTestCase(TestCase):
    """
    Tests for model methods and properties.
    Testes para métodos e propriedades dos modelos.
    """

    def setUp(self):
        """Set up test fixtures / Configura fixtures de teste"""
        self.user = User.objects.create_user(
            username="modeluser",
            email="model@example.com",
            password="testpass123",  # noqa: S106
        )
        self.product = Product.objects.create(
            name="Test Product", price="100.00", created_by=self.user
        )

    def test_product_is_new_property(self):
        """Test Product.is_new property / Testa propriedade Product.is_new"""
        self.assertTrue(self.product.is_new)

    def test_product_formatted_price(self):
        """Test Product.formatted_price property / Testa propriedade Product.formatted_price"""
        self.assertIn("100", self.product.formatted_price)

    def test_product_apply_discount(self):
        """Test Product.apply_discount() method / Testa método Product.apply_discount()"""
        from decimal import Decimal

        self.product.apply_discount(10)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, Decimal("90.00"))

    def test_product_deactivate(self):
        """Test Product.deactivate() method / Testa método Product.deactivate()"""
        self.product.deactivate()
        self.product.refresh_from_db()
        self.assertFalse(self.product.is_active)

    def test_product_activate(self):
        """Test Product.activate() method / Testa método Product.activate()"""
        self.product.is_active = False
        self.product.save()
        self.product.activate()
        self.product.refresh_from_db()
        self.assertTrue(self.product.is_active)


# Dummy view for testing rate limiting
# View de teste para o limite de taxa
@rate_limit(max_requests=2, period=10)
def rate_limited_test_view(request):
    """A simple view for testing the rate limit decorator."""
    return HttpResponse("Success")


urlpatterns = [
    path("test-rate-limit/", rate_limited_test_view),
]


@override_settings(ROOT_URLCONF=__name__)
class RateLimitDecoratorTest(TestCase):
    """
    Tests for the @rate_limit decorator.
    Testes para o decorador @rate_limit.
    """

    @override_settings(
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "LOCATION": "unique-snowflake-for-rate-limit-test",
            }
        }
    )
    def test_rate_limit_is_enforced(self):
        """
        Test that the rate limit decorator blocks requests after the limit is exceeded.
        Testa que o decorador de limite de taxa bloqueia requisições após o limite ser excedido.
        """
        from django.core.cache import cache

        cache.clear()

        # First 2 requests should be successful
        # As 2 primeiras requisições devem ser bem-sucedidas
        for _ in range(2):
            response = self.client.get("/test-rate-limit/")
            self.assertEqual(response.status_code, 200)

        # 3rd request should be blocked
        # A 3ª requisição deve ser bloqueada
        response = self.client.get("/test-rate-limit/")
        self.assertEqual(response.status_code, 429)
