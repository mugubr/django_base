from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Product

User = get_user_model()


class HelloAPITestCase(TestCase):
    """
    Tests for the hello_api view.
    Testes para a view hello_api.
    """

    def setUp(self):
        # setUp runs before each test method. We create a client
        # to make API requests.
        # setUp runs before each test method. We create a client t
        # o make API requests.
        self.client = APIClient()

    def test_hello_api_returns_correct_message(self):
        # Makes a GET request to the /api/v1/hello/ endpoint.
        # Faz uma requisição GET para o endpoint /api/v1/hello/.
        response = self.client.get("/api/v1/hello/")

        # Asserts that the HTTP status code is 200 OK.
        # Garante que o código de status HTTP é 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Asserts that the response data is the expected JSON.
        # Garante que os dados da resposta são o JSON esperado.
        self.assertEqual(
            response.data,
            {"message": "Olá, API do Projeto Base Django!"},
        )


class ProductModelTestCase(TestCase):
    """
    Tests for the Product model.
    Testes para o modelo Product.
    """

    def test_product_str_representation(self):
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
